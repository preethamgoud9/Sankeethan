
"""
Command-line interface for fetching and filtering PubMed papers.
"""
import argparse
import logging
import sys
from typing import List, Optional

from .pubmed_client import PubMedClient
from .affiliation_classifier import AffiliationClassifier
from .paper_processor import PaperProcessor
from .csv_formatter import CSVFormatter


def setup_logger(debug: bool = False) -> None:
    """
    Set up the logger.
    
    Args:
        debug: Whether to enable debug logging
    """
    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """
    Parse command-line arguments.
    
    Args:
        args: Command-line arguments
        
    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Fetch research papers from PubMed with authors affiliated with pharmaceutical or biotech companies."
    )
    
    parser.add_argument(
        "query",
        help="PubMed search query"
    )
    
    parser.add_argument(
        "-d", "--debug",
        action="store_true",
        help="Print debug information during execution"
    )
    
    parser.add_argument(
        "-f", "--file",
        help="Specify the filename to save the results. If not provided, print to console."
    )
    
    parser.add_argument(
        "--max-results",
        type=int,
        default=100,
        help="Maximum number of results to fetch (default: 100)"
    )
    
    return parser.parse_args(args)


def main(args: Optional[List[str]] = None) -> int:
    """
    Main entry point for the command-line interface.
    
    Args:
        args: Command-line arguments
        
    Returns:
        Exit code
    """
    parsed_args = parse_args(args)
    
    # Set up logging
    setup_logger(parsed_args.debug)
    logger = logging.getLogger(__name__)
    
    try:
        # Create the necessary objects
        client = PubMedClient()
        classifier = AffiliationClassifier()
        processor = PaperProcessor(client, classifier)
        formatter = CSVFormatter()
        
        # Get papers matching the query
        logger.info(f"Searching for papers with query: '{parsed_args.query}'")
        papers = processor.get_papers_with_company_affiliations(
            parsed_args.query, 
            max_results=parsed_args.max_results
        )
        
        if not papers:
            logger.warning("No papers found matching the criteria")
            return 0
            
        # Format the results as CSV
        logger.info(f"Found {len(papers)} papers with pharmaceutical/biotech company affiliations")
        
        # Write to file or print to console
        if parsed_args.file:
            formatter.format_papers(papers, parsed_args.file)
            logger.info(f"Results written to {parsed_args.file}")
        else:
            csv_output = formatter.format_papers(papers)
            print(csv_output)
            
        return 0
            
    except Exception as e:
        logger.error(f"Error: {e}")
        if parsed_args.debug:
            logger.exception("Detailed traceback:")
        return 1


def run_cli() -> None:
    """Function that Poetry will use as an entry point."""
    sys.exit(main())


if __name__ == "__main__":
    sys.exit(main())