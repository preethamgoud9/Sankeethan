"""
Module for classifying author affiliations as academic or non-academic.
"""
import logging
import re
from typing import Dict, List, Tuple, Set, Optional


class AffiliationClassifier:
    """
    Classifier for determining if an affiliation is academic or from a pharmaceutical/biotech company.
    """
    
    # Words that typically indicate academic institutions
    ACADEMIC_KEYWORDS = {
        "university", "college", "school", "institute", "academia", "faculty", 
        "department", "laboratory", "lab", "center for", "centre for", "hospital",
        "medical center", "medical centre", "clinic", "foundation", "institution",
        "national", "federal", "ministry", "association", "society"
    }
    
    # Words that indicate pharma/biotech companies
    COMPANY_KEYWORDS = {
        "inc.", "inc", "llc", "ltd", "limited", "corp", "corporation", "pharmaceuticals",
        "pharmaceutical", "pharma", "biotech", "biotechnology", "biopharmaceutical",
        "therapeutics", "biosciences", "biologics", "diagnostics", "laboratories",
        "medicines", "health products", "technologies", "genetics", "genomics",
        "company", "co.", "gmbh", "ag", "sa", "bv", "nv", "plc"
    }
    
    # Top pharmaceutical and biotech companies
    KNOWN_COMPANIES = {
        "pfizer", "johnson & johnson", "roche", "novartis", "merck", "gsk", 
        "glaxosmithkline", "sanofi", "abbvie", "bayer", "eli lilly", "bristol-myers squibb",
        "astrazeneca", "boehringer ingelheim", "amgen", "gilead", "teva", "novo nordisk",
        "takeda", "biogen", "celgene", "regeneron", "moderna", "biontech", "curevac",
        "genentech", "vertex", "alexion", "illumina", "incyte", "seagen", "biomarin",
        "alkermes", "ionis", "waters", "qiagen", "catalent", "lonza"
    }
    
    def __init__(self) -> None:
        """Initialize the classifier."""
        self.logger = logging.getLogger(__name__)
    
    def is_non_academic(self, affiliation: str) -> bool:
        """
        Determine if an affiliation is non-academic.
        
        Args:
            affiliation: The affiliation string to classify
            
        Returns:
            True if the affiliation appears to be from a non-academic institution,
            False otherwise
        """
        if not affiliation:
            return False
            
        affiliation_lower = affiliation.lower()
        
        # Check for known company names
        for company in self.KNOWN_COMPANIES:
            if company in affiliation_lower:
                return True
        
        # Check for company keywords
        for keyword in self.COMPANY_KEYWORDS:
            # Use word boundary to avoid partial matches
            if re.search(r'\b' + re.escape(keyword) + r'\b', affiliation_lower):
                # Check if it's not a university company/corporation
                if not any(re.search(r'\b' + re.escape(academic) + r'\b', affiliation_lower) 
                          for academic in self.ACADEMIC_KEYWORDS):
                    return True
        
        # Check for email domains that suggest companies
        email_match = re.search(r'[\w.-]+@([\w.-]+)', affiliation_lower)
        if email_match:
            domain = email_match.group(1)
            # Academic domains often end with .edu, .ac.xx, etc.
            if not any(domain.endswith(edu) for edu in ['.edu', '.ac.', '.edu.', '.ac.uk', '.gov']):
                # If it has company keywords in the domain, it's likely a company
                if any(company in domain for company in self.COMPANY_KEYWORDS):
                    return True
        
        return False
    
    def extract_company_name(self, affiliation: str) -> Optional[str]:
        """
        Extract the company name from the affiliation string.
        
        Args:
            affiliation: The affiliation string
            
        Returns:
            The extracted company name or None if not found
        """
        if not affiliation:
            return None
            
        affiliation_lower = affiliation.lower()
        
        # First check for known companies
        for company in self.KNOWN_COMPANIES:
            if company in affiliation_lower:
                # Find the actual case in the original string
                idx = affiliation_lower.find(company)
                if idx >= 0:
                    # Extract the company name with original capitalization
                    return affiliation[idx:idx+len(company)]
        
        # Look for company patterns like "XXX, Inc." or "XXX Ltd."
        company_pattern = re.search(r'([A-Za-z0-9\s&\-\.]+)(?:\s+(?:Inc\.?|LLC|Ltd\.?|Corp\.?|Corporation|GmbH|AG|BV|NV|S\.A\.))', affiliation)
        if company_pattern:
            return company_pattern.group(0).strip()
        
        # Look for company names in the affiliation text
        parts = [p.strip() for p in affiliation.split(',')]
        for part in parts:
            part_lower = part.lower()
            if any(keyword in part_lower for keyword in self.COMPANY_KEYWORDS) and \
               not any(academic in part_lower for academic in self.ACADEMIC_KEYWORDS):
                return part.strip()
        
        # If no clear company name is found, return the first part of the affiliation
        # This is a fallback and might not be accurate
        if parts:
            return parts[0].strip()
            
        return None