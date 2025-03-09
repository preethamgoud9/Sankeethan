"""
Module for processing paper data from PubMed.
"""
import logging
from typing import Dict, List, Any, Optional, Set

from .pubmed_client import PubMedClient
from .affiliation_classifier import AffiliationClassifier


class PaperProcessor:
    """
    Process paper data retrieved from PubMed.
    """
    
    def __init__(self, client: Optional[PubMedClient] = None, 
                 classifier: Optional[AffiliationClassifier] = None) -> None:
        """
        Initialize the paper processor.
        
        Args:
            client: PubMed client instance
            classifier: Affiliation classifier instance
        """
        self.logger = logging.getLogger(__name__)
        self.client = client or PubMedClient()
        self.classifier = classifier or AffiliationClassifier()
    
    def get_papers_with_company_affiliations(self, query: str, max_results: int = 100) -> List[Dict[str, Any]]:
        """
        Get papers matching the query with at least one pharma/biotech company affiliation.
        
        Args:
            query: PubMed search query
            max_results: Maximum number of results to return
            
        Returns:
            List of papers with company affiliations
        """
        self.logger.info(f"Searching for papers with query: '{query}'")
        
        # Search for papers
        pmids = self.client.search_papers(query, max_results)
        
        if not pmids:
            self.logger.warning("No papers found for the given query")
            return []
            
        self.logger.info(f"Found {len(pmids)} papers. Fetching details and filtering for company affiliations...")
        
        results = []
        for pmid in pmids:
            try:
                # Fetch paper details
                paper_details = self.client.fetch_paper_details(pmid)
                
                # Process the paper to extract non-academic authors
                processed_paper = self._process_paper(paper_details)
                
                # Add to results if there are non-academic authors
                if processed_paper and processed_paper.get("non_academic_authors"):
                    results.append(processed_paper)
                    
            except Exception as e:
                self.logger.error(f"Error processing paper {pmid}: {e}")
                continue
                
        self.logger.info(f"Found {len(results)} papers with company affiliations")
        return results
    
    def _process_paper(self, paper_details: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process paper details to extract non-academic authors.
        
        Args:
            paper_details: Paper details from PubMed
            
        Returns:
            Processed paper with non-academic authors and their affiliations
        """
        processed_paper = {
            "pmid": paper_details.get("pmid", ""),
            "title": paper_details.get("title", ""),
            "publication_date": paper_details.get("publication_date", ""),
            "non_academic_authors": [],
            "company_affiliations": set(),  # Using a set to avoid duplicates
            "corresponding_author_email": paper_details.get("corresponding_author_email", "")
        }
        
        # Process each author
        for author in paper_details.get("authors", []):
            non_academic_affiliations = []
            
            # Check each affiliation
            for affiliation in author.get("affiliations", []):
                if self.classifier.is_non_academic(affiliation):
                    non_academic_affiliations.append(affiliation)
                    
                    # Extract company name
                    company_name = self.classifier.extract_company_name(affiliation)
                    if company_name:
                        processed_paper["company_affiliations"].add(company_name)
            
            # If author has non-academic affiliations, add to the list
            if non_academic_affiliations:
                author_name = f"{author.get('first_name', '')} {author.get('last_name', '')}".strip()
                if author_name:
                    processed_paper["non_academic_authors"].append({
                        "name": author_name,
                        "affiliations": non_academic_affiliations
                    })
        
        # Convert set to list
        processed_paper["company_affiliations"] = list(processed_paper["company_affiliations"])
        
        return processed_paper