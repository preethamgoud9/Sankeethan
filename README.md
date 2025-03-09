# PubMed Papers

A Python command-line tool for fetching research papers from PubMed with authors affiliated with pharmaceutical or biotech companies.

## Overview

This tool searches PubMed for papers based on user-specified queries, identifies papers with at least one author affiliated with a pharmaceutical or biotech company, and outputs the results as a CSV file with the required columns.

## Features

- Search PubMed using its full query syntax
- Identify authors affiliated with pharmaceutical or biotech companies
- Extract corresponding author emails
- Output results as a CSV file with the following columns:
  - PubmedID
  - Title
  - Publication Date
  - Non-academic Author(s)
  - Company Affiliation(s)
  - Corresponding Author Email

## Installation

### Prerequisites

- Python 3.8 or higher
- [Poetry](https://python-poetry.org/docs/#installation) package manager

### Setup

```bash
# Clone the repository
git clone https://github.com/preethamgoud9/Sankeethan.git
cd Sankeethan

# Install dependencies
poetry install
```

## Sankeerthan

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/preethamgoud9/Sankeethan.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Sankeerthan
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
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

PubMed supports complex queries:

- Simple keyword search: `"cancer"`
- Multiple keywords: `

### Sankeerthan Usage

To process PubMed papers, run the following scripts:

1. **Fetch Papers**:
   ```bash
   python pubmed_papers/pubmed_client.py
   ```
2. **Process Papers**:
   ```bash
   python pubmed_papers/paper_processor.py
   ```
3. **Format Results**:
   ```bash
   python pubmed_papers/csv_formatter.py
   ```

## Output

The processed results will be saved in `results.csv`.