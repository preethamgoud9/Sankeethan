"""
PubMed Papers - A tool for fetching research papers from PubMed with authors 
affiliated with pharmaceutical or biotech companies.
"""

from .pubmed_client import PubMedClient
from .affiliation_classifier import AffiliationClassifier
from .paper_processor import PaperProcessor
from .csv_formatter import CSVFormatter

__version__ = "0.1.0"