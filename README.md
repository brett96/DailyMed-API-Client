# DailyMed API Python Client

Lightweight command-line client for the DailyMed v2 REST API — search SPLs, fetch raw SPL XML, parse ingredients, and list related resources.

---

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Help](#getting-help)
  - [Basic Examples](#basic-examples)
  - [Advanced / Custom Search](#advanced--custom-search)
- [Notes](#notes)

---

## Features

- Advanced multi-step search with post-filtering (route, include/exclude active/inactive ingredients).
- Direct API searches (search-spls) with many filters (drug name, NDC, boxed warning, etc.).
- Parse SPL ingredients into readable active / inactive lists (get-ingredients).
- Retrieve raw SPL XML (get-spl) and related info:
  - Version history (get-spl-history)
  - Associated NDCs (get-spl-ndcs)
  - Packaging info (get-spl-packaging)
- List/filter core resources:
  - Drug names (get-drugnames)
  - NDCs (get-ndcs)
  - Drug classes (get-drugclasses)
  - UNIIs (get-uniis)
  - RxCUIs (get-rxcuis)
- Single-file script, only requires `requests`.
- Error handling for common network/API issues.

---

## Requirements

- Python 3.10+
- requests (see requirements.txt)
- Windows / macOS / Linux

---

## Installation

```bash
git clone https://github.com/brett96/DailyMed-API-Client
cd DailyMed-API-Client
```

Create and activate a virtualenv:

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

### Getting help

```bash
python dailymed_client.py --help
python dailymed_client.py search-spls --help
python dailymed_client.py search --help
```

### Basic Examples

Search SPLs (first 5):

```bash
python dailymed_client.py search-spls --drug_name aspirin --pagesize 5
```

Get raw SPL XML by SET ID:

```bash
python dailymed_client.py get-spl "37e939c6-064b-3548-e063-6294a90a337d"
```

Get parsed ingredients (WIP):

```bash
python dailymed_client.py get-ingredients "37e939c6-064b-3548-e063-6294a90a337d"
```

View SPL version history:

```bash
python dailymed_client.py get-spl-history "a810d7c6-3b8f-4354-8e8a-02c1d21f845a"
```

List drug names (first 10):

```bash
python dailymed_client.py get-drugnames --pagesize 10
```

---

## Advanced / Custom Search

The `search` command performs an initial API search (by drug name, etc.), then fetches each SPL to apply post-filters. This is multi-step and may be slower.

Examples:

1) Route filter (processes first 10 results):

```bash
python dailymed_client.py search --drug_name "ibuprofen" --route "ORAL" --pagesize 10
```

2) Include / exclude active ingredients (processes first 20 results):

```bash
python dailymed_client.py search --drug_name "tylenol" \
  --include-active "Guaifenesin" \
  --exclude-active "Dextromethorphan" \
  --pagesize 20
```

3) Find products with a specific inactive ingredient:

```bash
python dailymed_client.py search --drug_name "acetaminophen" --include-inactive "aspartame" --pagesize 15
```

4) Complex filters (multiple excludes):

```bash
python dailymed_client.py search --drug_name "loratadine" --route "ORAL" --exclude-inactive "sucralose" "aspartame"
```

---
