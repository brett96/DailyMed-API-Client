DailyMed API Python ClientThis project is a command-line Python script (dailymed_client.py) that demonstrates how to interact with the official DailyMed v2 RESTful API. It allows you to search for drug labels (SPLs), retrieve specific SPL details, and list various resources like drug names, NDCs, and drug classes.This client is written for Python 3.10+ and is compatible with Python 3.13.5 on Windows, macOS, and Linux.FeaturesSearch for drug labels (SPLs) by drug name or NDC.Retrieve a specific SPL document by its SET ID.Get related SPL information:Version HistoryAssociated NDCsPackaging InformationList core DailyMed resources:Drug NamesNDCsDrug ClassesUnique Ingredient Identifiers (UNIIs)Simple, self-contained script with no external dependencies besides requests.Includes error handling for common network and API issues.PrerequisitesPython 3.10 or newer (tested with 3.13.5)The requests libraryInstallationClone or download:Save the dailymed_client.py, requirements.txt, and README.md files into a new directory (e.g., dailymed-project).Create a virtual environment (Recommended):Open a terminal or command prompt in your project directory and run:# On Windows
python -m venv venv
.\venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
Install dependencies:With your virtual environment active, install the required requests library:pip install -r requirements.txt
UsageThe script is run from the command line using python dailymed_client.py followed by a command and its options.You can see all available commands by running:python dailymed_client.py --help
Example CommandsHere are some examples of how to use the tool.1. Search for a drug label (SPL):This searches for SPLs matching the drug name "aspirin" and returns the first 5 results.python dailymed_client.py search-spls --drug_name aspirin --pagesize 5
2. Get a specific SPL document:Once you have a set_id from a search, you can retrieve the full SPL document. (This set_id is just an example).python dailymed_client.py get-spl "a810d7c6-3b8f-4354-8e8a-02c1d21f845a"
3. Get the history for an SPL:See all the versions for a specific set_id.python dailymed_client.py get-spl-history "a810d7c6-3b8f-4354-8e8a-02c1d21f845a"
4. Get packaging info for an SPL:python dailymed_client.py get-spl-packaging "a810d7c6-3b8f-4354-8e8a-02c1d21f845a"
5. List the first 10 drug names in the database:python dailymed_client.py get-drugnames --pagesize 10
6. List the first 10 drug classes:python dailymed_client.py get-drugclasses --pagesize 10
