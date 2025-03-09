"""
PubMed API client for fetching research papers.
"""
import logging
import time
from typing import Dict, List, Optional, Any
import urllib.parse
import urllib.request
import json
import xml.etree.ElementTree as ET


class PubMedClient:
    """Client for interacting with the PubMed API."""
    
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    SEARCH_URL = f"{BASE_URL}/esearch.fcgi"
    FETCH_URL = f"{BASE_URL}/efetch.fcgi"
    SUMMARY_URL = f"{BASE_URL}/esummary.fcgi"
    
    def __init__(self, email: str = "your-email@example.com", tool: str = "pubmed-papers-tool", 
                 delay: float = 0.34) -> None:
        """
        Initialize the PubMed client.
        
        Args:
            email: Email to identify your requests to NCBI
            tool: Tool name to identify your requests
            delay: Delay between requests to comply with NCBI's rate limits (in seconds)
        """
        self.email = email
        self.tool = tool
        self.delay = delay
        self.logger = logging.getLogger(__name__)
    
    def search_papers(self, query: str, max_results: int = 100) -> List[str]:
        """
        Search for papers using the provided query.
        
        Args:
            query: PubMed search query
            max_results: Maximum number of results to return
            
        Returns:
            List of PubMed IDs matching the query
        """
        self.logger.debug(f"Searching for papers with query: {query}")
        
        # URL encode the query
        encoded_query = urllib.parse.quote_plus(query)
        
        # Build the search URL
        params = {
            "db": "pubmed",
            "term": encoded_query,
            "retmode": "json",
            "retmax": max_results,
            "usehistory": "y",
            "tool": self.tool,
            "email": self.email
        }
        
        search_url = f"{self.SEARCH_URL}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
        
        try:
            with urllib.request.urlopen(search_url) as response:
                search_results = json.load(response)
                
            # Extract the PubMed IDs
            if "esearchresult" in search_results and "idlist" in search_results["esearchresult"]:
                pmids = search_results["esearchresult"]["idlist"]
                self.logger.debug(f"Found {len(pmids)} papers")
                return pmids
            else:
                self.logger.warning("No results found or unexpected response format")
                return []
                
        except Exception as e:
            self.logger.error(f"Error searching for papers: {e}")
            raise
            
        finally:
            # Respect NCBI's rate limits
            time.sleep(self.delay)
    
    def fetch_paper_details(self, pmid: str) -> Dict[str, Any]:
        """
        Fetch detailed information for a specific paper.
        
        Args:
            pmid: PubMed ID of the paper
            
        Returns:
            Dictionary containing paper details
        """
        self.logger.debug(f"Fetching details for PMID: {pmid}")
        
        params = {
            "db": "pubmed",
            "id": pmid,
            "retmode": "xml",
            "tool": self.tool,
            "email": self.email
        }
        
        fetch_url = f"{self.FETCH_URL}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
        
        try:
            with urllib.request.urlopen(fetch_url) as response:
                xml_data = response.read()
                
            # Parse the XML response
            root = ET.fromstring(xml_data)
            
            # Extract paper details
            article_data = self._parse_article_xml(root)
            return article_data
                
        except Exception as e:
            self.logger.error(f"Error fetching paper details for PMID {pmid}: {e}")
            raise
            
        finally:
            # Respect NCBI's rate limits
            time.sleep(self.delay)
    
    def _parse_article_xml(self, root: ET.Element) -> Dict[str, Any]:
        """
        Parse the XML response from PubMed to extract article details.
        
        Args:
            root: XML root element
            
        Returns:
            Dictionary containing parsed article data
        """
        result = {
            "pmid": "",
            "title": "",
            "publication_date": "",
            "authors": [],
            "corresponding_author_email": ""
        }
        
        # Find PubmedArticle element
        pubmed_article = root.find(".//PubmedArticle")
        if pubmed_article is None:
            return result
            
        # Extract PMID
        pmid_elem = pubmed_article.find(".//PMID")
        if pmid_elem is not None and pmid_elem.text:
            result["pmid"] = pmid_elem.text
            
        # Extract title
        title_elem = pubmed_article.find(".//ArticleTitle")
        if title_elem is not None and title_elem.text:
            result["title"] = title_elem.text
            
        # Extract publication date
        pub_date_elem = pubmed_article.find(".//PubDate")
        if pub_date_elem is not None:
            year = pub_date_elem.find("Year")
            month = pub_date_elem.find("Month")
            day = pub_date_elem.find("Day")
            
            year_text = year.text if year is not None and year.text else ""
            month_text = month.text if month is not None and month.text else ""
            day_text = day.text if day is not None and day.text else ""
            
            if year_text:
                if month_text and day_text:
                    result["publication_date"] = f"{year_text}-{month_text}-{day_text}"
                elif month_text:
                    result["publication_date"] = f"{year_text}-{month_text}"
                else:
                    result["publication_date"] = year_text
        
        # Extract authors and affiliations
        author_list = pubmed_article.find(".//AuthorList")
        if author_list is not None:
            for author_elem in author_list.findall("Author"):
                author_data = self._parse_author(author_elem)
                if author_data:
                    result["authors"].append(author_data)
                    
                    # Check if this is the corresponding author
                    if author_data.get("is_corresponding", False) and author_data.get("email"):
                        result["corresponding_author_email"] = author_data["email"]
        
        return result
        
    def _parse_author(self, author_elem: ET.Element) -> Dict[str, Any]:
        """
        Parse author information from XML.
        
        Args:
            author_elem: XML element containing author data
            
        Returns:
            Dictionary with author details
        """
        author_data = {
            "last_name": "",
            "first_name": "",
            "initials": "",
            "affiliations": [],
            "email": "",
            "is_corresponding": False
        }
        
        # Extract name components
        last_name = author_elem.find("LastName")
        if last_name is not None and last_name.text:
            author_data["last_name"] = last_name.text
            
        first_name = author_elem.find("ForeName")
        if first_name is not None and first_name.text:
            author_data["first_name"] = first_name.text
            
        initials = author_elem.find("Initials")
        if initials is not None and initials.text:
            author_data["initials"] = initials.text
            
        # Extract affiliations
        affiliations = author_elem.findall(".//Affiliation")
        for affiliation in affiliations:
            if affiliation.text:
                author_data["affiliations"].append(affiliation.text)
                
                # Check if email is in the affiliation text
                # Emails are often included in the affiliation text
                text = affiliation.text.lower()
                if "@" in text and "." in text:
                    email_parts = [part for part in text.split() if "@" in part]
                    if email_parts:
                        # Clean up email (remove punctuation)
                        email = email_parts[0].strip(".,;:()")
                        author_data["email"] = email
                        # Assume authors with emails are corresponding authors
                        author_data["is_corresponding"] = True
        
        # If no full name available, use initials
        if not author_data["first_name"] and author_data["initials"]:
            author_data["first_name"] = author_data["initials"]
            
        return author_data