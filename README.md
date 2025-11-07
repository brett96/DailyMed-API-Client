# DailyMed API Python Client

A command-line Python script that interacts with the official DailyMed v2 RESTful API to search drug labels, retrieve SPL details, and list various drug-related resources.

## Requirements

- Python 3.10+ (compatible with Python 3.13.5)
- Windows, macOS, or Linux
- `requests` library

## Features

- **Search drug labels (SPLs)** by drug name or NDC
- **Retrieve specific SPL documents** by SET ID
- **Access related SPL information:**
  - Version History
  - Associated NDCs
  - Packaging Information
- **List core DailyMed resources:**
  - Drug Names
  - NDCs
  - Drug Classes
  - Unique Ingredient Identifiers (UNIIs)
- Simple, self-contained script with minimal dependencies
- Built-in error handling for network and API issues

## Installation

1. **Clone or download:**
   ```bash
   git clone <repository-url>
   cd dailymed-project
   ```

2. **Create a virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

View available commands:
```bash
python dailymed_client.py --help
```

### Example Commands

#### 1. Search for drug labels
Search for SPLs matching "aspirin" (first 5 results):
```bash
python dailymed_client.py search-spls --drug_name aspirin --pagesize 5
```

#### 2. Get specific SPL document
Retrieve full SPL document by SET ID:
```bash
python dailymed_client.py get-spl "a810d7c6-3b8f-4354-8e8a-02c1d21f845a"
```

#### 3. View SPL history
See all versions for a specific SET ID:
```bash
python dailymed_client.py get-spl-history "a810d7c6-3b8f-4354-8e8a-02c1d21f845a"
```

#### 4. Get packaging information
```bash
python dailymed_client.py get-spl-packaging "a810d7c6-3b8f-4354-8e8a-02c1d21f845a"
```

#### 5. List drug names
Display first 10 drug names:
```bash
python dailymed_client.py get-drugnames --pagesize 10
```

#### 6. List drug classes
Display first 10 drug classes:
```bash
python dailymed_client.py get-drugclasses --pagesize 10
```
