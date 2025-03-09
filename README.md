
# PubMed Papers

A Python command-line tool for fetching research papers from PubMed with authors affiliated with pharmaceutical or biotech companies.

## Overview

This tool allows you to search for papers on PubMed and identify those with at least one author affiliated with a pharmaceutical or biotech company. The results are returned as a CSV file.

## Features

- Search PubMed using its full query syntax
- Identify authors affiliated with pharmaceutical or biotech companies
- Extract corresponding author emails
- Output results as a CSV file or to the console

## Installation

### Prerequisites

- Python 3.8 or higher
- [Poetry](https://python-poetry.org/docs/#installation) package manager

### Installing with Poetry

```bash
# Clone the repository
git clone https://github.com/yourusername/pubmed-papers.git
cd pubmed-papers

# Install dependencies
poetry install
```

## Usage

```bash
# Display help
poetry run get-papers-list --help

# Basic usage
poetry run get-papers-list "cancer immunotherapy"

# Save results to a file
poetry run get-papers-list "cancer immunotherapy" --file results.csv

# Enable debug logging
poetry run get-papers-list "cancer immunotherapy" --debug

# Limit the number of results
poetry run get-papers-list "cancer immunotherapy" --max-results 50
```

### Example Queries

PubMed supports complex queries. Here are some examples:

- Simple keyword search: `"cancer"`
- Multiple keywords: `"cancer immunotherapy"`
- Author search: `"Smith J[Author]"`
- Date range: `"2020[pdat]:2023[pdat]"`
- Journal search: `"Nature[Journal]"`
- Combining terms: `"cancer AND immunotherapy AND 2020[pdat]:2023[pdat]"`

## Project Structure

- `pubmed_papers/`
  - `__init__.py`: Package initialization
  - `cli.py`: Command-line interface
  - `pubmed_client.py`: Client for the PubMed API
  - `affiliation_classifier.py`: Logic for identifying non-academic affiliations
  - `paper_processor.py`: Processing paper data
  - `csv_formatter.py`: Formatting results as CSV

## Development

### Running Tests

```bash
poetry run pytest
```

### Type Checking

```bash
poetry run mypy pubmed_papers
```

### Code Formatting

```bash
poetry run black pubmed_papers
```

## Tools Used

- [Poetry](https://python-poetry.org/): Dependency management and packaging
- [PubMed API (E-utilities)](https://www.# Sankeethan
