"""
Module for formatting paper data as CSV.
"""
import csv
import io
import logging
import sys
from typing import Dict, List, Any, TextIO, Optional


class CSVFormatter:
    """
    Format paper data as CSV.
    """
    
    CSV_HEADERS = [
        "PubmedID", 
        "Title", 
        "Publication Date", 
        "Non-academic Author(s)", 
        "Company Affiliation(s)", 
        "Corresponding Author Email"
    ]
    
    def __init__(self) -> None:
        """Initialize the CSV formatter."""
        self.logger = logging.getLogger(__name__)
    
    def format_papers(self, papers: List[Dict[str, Any]], output_file: Optional[str] = None) -> str:
        """
        Format papers as CSV.
        
        Args:
            papers: List of paper data to format
            output_file: Optional file path to write to
            
        Returns:
            CSV string if output_file is None, otherwise empty string
        """
        if not papers:
            self.logger.warning("No papers to format")
            return ""
            
        # Use StringIO if no output file specified
        if output_file is None:
            output = io.StringIO()
            self._write_csv(papers, output)
            return output.getvalue()
        else:
            try:
                with open(output_file, 'w', newline='', encoding='utf-8') as file:
                    self._write_csv(papers, file)
                self.logger.info(f"CSV output written to {output_file}")
                return ""
            except Exception as e:
                self.logger.error(f"Error writing to {output_file}: {e}")
                raise
    
    def _write_csv(self, papers: List[Dict[str, Any]], output: TextIO) -> None:
        """
        Write papers to CSV format.
        
        Args:
            papers: List of paper data
            output: File-like object to write to
        """
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(self.CSV_HEADERS)
        
        # Write data rows
        for paper in papers:
            # Format non-academic authors
            author_names = [author["name"] for author in paper.get("non_academic_authors", [])]
            authors_str = "; ".join(author_names)
            
            # Format company affiliations
            affiliations_str = "; ".join(paper.get("company_affiliations", []))
            
            writer.writerow([
                paper.get("pmid", ""),
                paper.get("title", ""),
                paper.get("publication_date", ""),
                authors_str,
                affiliations_str,
                paper.get("corresponding_author_email", "")
            ])