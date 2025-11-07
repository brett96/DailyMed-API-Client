# DailyMed API Python Client

A command-line Python script that interacts with the official DailyMed v2 RESTful API to search drug labels, retrieve SPL details, and list various drug-related resources.

## Requirements

- Python 3.10+ (compatible with Python 3.13.5)
- Windows, macOS, or Linux
- `requests` library

## Features

**Search Capabilities**
- Search drug labels (SPLs) by drug name, NDC, labeler, RxCUI, and many other advanced filters
- Retrieve specific SPL documents by SET ID

**SPL Information Access**
- Version History
- Associated NDCs
- Packaging Information

**Resource Management**
- Drug Names (filter by manufacturer, name type)
- NDCs (filter by labeler, application number)
- Drug Classes (filter by class name, class type)
- Unique Ingredient Identifiers (UNIIs)
- RxNorm Concept Unique Identifiers (RxCUIs)

**Technical Features**
- Simple, self-contained script
- Only requires `requests` library
- Built-in error handling for network and API issues

## Installation

1. **Clone or download:**
   ```bash
   git clone https://github.com/brett96/DailyMed-API-Client
   cd DailyMed-API-Client
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

### Getting Help
```bash
# View all commands
python dailymed_client.py --help

# Get help for specific commands
python dailymed_client.py search-spls --help
python dailymed_client.py get-rxcuis --help
```

### Basic Examples

1. **Search for drug labels**
   ```bash
   # Search for "aspirin" (first 5 results)
   python dailymed_client.py search-spls --drug_name aspirin --pagesize 5
   ```

2. **Retrieve SPL document**
   ```bash
   # Get full SPL document by SET ID
   python dailymed_client.py get-spl "a810d7c6-3b8f-4354-8e8a-02c1d21f845a"
   ```

3. **View SPL history**
   ```bash
   python dailymed_client.py get-spl-history "a810d7c6-3b8f-4354-8e8a-02c1d21f845a"
   ```

4. **List drug names**
   ```bash
   # Display first 10 drug names
   python dailymed_client.py get-drugnames --pagesize 10
   ```

### Advanced Examples

1. **Find SPLs with boxed warning**
   ```bash
   python dailymed_client.py search-spls --drug_name "ibuprofen" --boxed_warning True
   ```

2. **Search by manufacturer**
   ```bash
   python dailymed_client.py get-drugnames --manufacturer "Pfizer" --name_type "b"
   ```

3. **List drug classes**
   ```bash
   python dailymed_client.py get-drugclasses --class_code_type "moa" --pagesize 20
   ```

4. **Search by date**
   ```bash
   python dailymed_client.py search-spls --published_date "2023-10-01" --published_date_comparison "eq"
   ```

5. **Search by ingredient**
   ```bash
   # Find SPLs containing Acetaminophen
   python dailymed_client.py search-spls --unii_code "362O9ITL9D"
   ```

6. **Search RxCUI codes**
   ```bash
   # Find RxCUI codes for "aspirin" ('Prescribable Name' only)
   python dailymed_client.py get-rxcuis --rxstring "aspirin" --rxtty "PSN"
   ```
