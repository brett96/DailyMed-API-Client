import requests
import json
import argparse
import sys
from typing import Dict, Any, Optional, Union

class DailyMedAPI:
    """
    A Python client for interacting with the DailyMed RESTful API (v2).
    
    This client provides methods to access various endpoints of the DailyMed API,
    handling HTTP requests and JSON responses.
    """
    
    BASE_URL = "https://dailymed.nlm.nih.gov/dailymed/services/v2"

    def _add_if_present(self, params: Dict[str, Any], key: str, value: Optional[Any]):
        """Helper to add a parameter to the dict if it's not None."""
        if value is not None:
            params[key] = value

    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Union[Dict[str, Any], str]:
        """
        Internal helper method to make a GET request to the DailyMed API.

        Args:
            endpoint: The API endpoint to call (e.g., "spls.json").
            params: A dictionary of query parameters for the request.

        Returns:
            A dictionary parsed from the JSON response or an XML string.
            
        Raises:
            requests.exceptions.HTTPError: If the API returns an error status code.
            requests.exceptions.RequestException: For other network or request-related issues.
            json.JSONDecodeError: If the response is not valid JSON.
        """
        
        # Clean params dictionary of None values
        clean_params = {}
        if params:
            for key, value in params.items():
                if value is not None:
                    clean_params[key] = value
        
        url = f"{self.BASE_URL}/{endpoint}"
        
        try:
            response = requests.get(url, params=clean_params, timeout=10)
            # Raise an exception for bad status codes (4xx or 5xx)
            response.raise_for_status()
            
            # Handle XML endpoint specifically
            if endpoint.endswith(".xml"):
                return response.text

            # Handle JSON endpoints (default)
            # Handle potential empty responses for some endpoints
            if not response.content:
                return {"message": "Request successful, but no content returned."}
                
            return response.json()
        
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err} - {response.status_code} {response.text}", file=sys.stderr)
            raise
        except requests.exceptions.ConnectionError as conn_err:
            print(f"Connection error occurred: {conn_err}", file=sys.stderr)
            raise
        except requests.exceptions.Timeout as timeout_err:
            print(f"Timeout error occurred: {timeout_err}", file=sys.stderr)
            raise
        except requests.exceptions.RequestException as req_err:
            print(f"An unexpected error occurred: {req_err}", file=sys.stderr)
            raise
        except json.JSONDecodeError:
            print(f"Failed to decode JSON response from {url}", file=sys.stderr)
            print(f"Response text: {response.text[:200]}...", file=sys.stderr)
            raise

    def search_spls(
        self, 
        page: int = 1, 
        pagesize: int = 10,
        application_number: Optional[str] = None,
        boxed_warning: Optional[bool] = None,
        dea_schedule_code: Optional[str] = None,
        doctype: Optional[str] = None,
        drug_class_code: Optional[str] = None,
        drug_class_coding_system: Optional[str] = None,
        drug_name: Optional[str] = None,
        name_type: Optional[str] = None,
        labeler: Optional[str] = None,
        manufacturer: Optional[str] = None,
        marketing_category_code: Optional[str] = None,
        ndc: Optional[str] = None,
        published_date: Optional[str] = None,
        published_date_comparison: Optional[str] = None,
        rxcui: Optional[str] = None,
        setid: Optional[str] = None,
        unii_code: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Searches for Structured Product Labeling (SPLs) documents with advanced filters.
        """
        print(f"\nSearching SPLs (Page {page}, Size {pagesize}) with filters...")
        
        params = {"page": page, "pagesize": pagesize}
        self._add_if_present(params, 'application_number', application_number)
        self._add_if_present(params, 'boxed_warning', boxed_warning)
        self._add_if_present(params, 'dea_schedule_code', dea_schedule_code)
        self._add_if_present(params, 'doctype', doctype)
        self._add_if_present(params, 'drug_class_code', drug_class_code)
        self._add_if_present(params, 'drug_class_coding_system', drug_class_coding_system)
        self._add_if_present(params, 'drug_name', drug_name)
        self._add_if_present(params, 'name_type', name_type)
        self._add_if_present(params, 'labeler', labeler)
        self._add_if_present(params, 'manufacturer', manufacturer)
        self._add_if_present(params, 'marketing_category_code', marketing_category_code)
        self._add_if_present(params, 'ndc', ndc)
        self._add_if_present(params, 'published_date', published_date)
        self._add_if_present(params, 'published_date_comparison', published_date_comparison)
        self._add_if_present(params, 'rxcui', rxcui)
        self._add_if_present(params, 'setid', setid)
        self._add_if_present(params, 'unii_code', unii_code)

        return self._make_request("spls.json", params=params)

    def get_spl_by_setid(self, set_id: str) -> str:
        """
        Retrieves a specific SPL document using its SET ID.
        This endpoint returns a raw XML string.
        
        Args:
            set_id: The SET ID of the SPL document.

        Returns:
            The XML response string from the API.
        """
        print(f"\nGetting SPL for SET ID: {set_id}...")
        return self._make_request(f"spls/{set_id}.xml", params=None)

    def get_spl_history(self, set_id: str) -> Dict[str, Any]:
        """
        Retrieves the version history for a specific SPL.
        """
        print(f"\nGetting SPL history for SET ID: {set_id}...")
        return self._make_request(f"spls/{set_id}/history.json", params=None)

    def get_spl_ndcs(self, set_id: str) -> Dict[str, Any]:
        """
        Retrieves all NDCs associated with a specific SPL.
        """
        print(f"\nGetting NDCs for SET ID: {set_id}...")
        return self._make_request(f"spls/{set_id}/ndcs.json", params=None)

    def get_spl_packaging(self, set_id: str) -> Dict[str, Any]:
        """
        Retrieves product packaging information for a specific SPL.
        """
        print(f"\nGetting packaging info for SET ID: {set_id}...")
        return self._make_request(f"spls/{set_id}/packaging.json", params=None)

    def get_drug_names(
        self, 
        page: int = 1, 
        pagesize: int = 10,
        manufacturer: Optional[str] = None,
        name_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Retrieves a list of all drug names, with optional filters.
        """
        print(f"\nGetting drug names (Page {page}, Size {pagesize})...")
        params = {"page": page, "pagesize": pagesize}
        self._add_if_present(params, 'manufacturer', manufacturer)
        self._add_if_present(params, 'name_type', name_type)
        return self._make_request("drugnames.json", params=params)

    def get_ndcs(
        self, 
        page: int = 1, 
        pagesize: int = 10,
        application_number: Optional[str] = None,
        labeler: Optional[str] = None,
        marketing_category_code: Optional[str] = None,
        setid: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Retrieves a list of all NDCs, with optional filters.
        """
        print(f"\nGetting NDCs (Page {page}, Size {pagesize})...")
        params = {"page": page, "pagesize": pagesize}
        self._add_if_present(params, 'application_number', application_number)
        self._add_if_present(params, 'labeler', labeler)
        self._add_if_present(params, 'marketing_category_code', marketing_category_code)
        self._add_if_present(params, 'setid', setid)
        return self._make_request("ndcs.json", params=params)

    def get_drug_classes(
        self, 
        page: int = 1, 
        pagesize: int = 10,
        drug_class_code: Optional[str] = None,
        drug_class_coding_system: Optional[str] = None,
        class_code_type: Optional[str] = None,
        class_name: Optional[str] = None,
        unii_code: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Retrieves a list of all drug classes, with optional filters.
        """
        print(f"\nGetting drug classes (Page {page}, Size {pagesize})...")
        params = {"page": page, "pagesize": pagesize}
        self._add_if_present(params, 'drug_class_code', drug_class_code)
        self._add_if_present(params, 'drug_class_coding_system', drug_class_coding_system)
        self._add_if_present(params, 'class_code_type', class_code_type)
        self._add_if_present(params, 'class_name', class_name)
        self._add_if_present(params, 'unii_code', unii_code)
        return self._make_request("drugclasses.json", params=params)

    def get_uniis(
        self, 
        page: int = 1, 
        pagesize: int = 10,
        active_moiety: Optional[str] = None,
        drug_class_code: Optional[str] = None,
        drug_class_coding_system: Optional[str] = None,
        rxcui: Optional[str] = None,
        unii_code: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Retrieves a list of all Unique Ingredient Identifiers (UNIIs), with optional filters.
        """
        print(f"\nGetting UNIIs (Page {page}, Size {pagesize})...")
        params = {"page": page, "pagesize": pagesize}
        self._add_if_present(params, 'active_moiety', active_moiety)
        self._add_if_present(params, 'drug_class_code', drug_class_code)
        self._add_if_present(params, 'drug_class_coding_system', drug_class_coding_system)
        self._add_if_present(params, 'rxcui', rxcui)
        self._add_if_present(params, 'unii_code', unii_code)
        return self._make_request("uniis.json", params=params)

    def get_rxcuis(
        self,
        page: int = 1,
        pagesize: int = 10,
        rxcui: Optional[str] = None,
        rxstring: Optional[str] = None,
        rxtty: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Retrieves a list of all RxNorm Concept Unique Identifiers (RxCUIs), with optional filters.
        """
        print(f"\nGetting RxCUIs (Page {page}, Size {pagesize})...")
        params = {"page": page, "pagesize": pagesize}
        self._add_if_present(params, 'rxcui', rxcui)
        self._add_if_present(params, 'rxstring', rxstring)
        self._add_if_present(params, 'rxtty', rxtty)
        return self._make_request("rxcuis.json", params=params)

def pretty_print_json(data: Dict[str, Any]):
    """Helper function to print JSON data in an indented, readable format."""
    print(json.dumps(data, indent=2))

def main():
    """
    Main function to run the command-line interface for the DailyMed API client.
    """
    # Main parser
    parser = argparse.ArgumentParser(
        description="A command-line client for the DailyMed v2 API.",
        epilog="Example: python dailymed_client.py search-spls --drug_name aspirin"
    )
    subparsers = parser.add_subparsers(dest="command", required=True, help="The API command to run")

    # --- search-spls command ---
    spl_parser = subparsers.add_parser("search-spls", help="Search for SPLs (drug labels).")
    spl_parser.add_argument("--page", type=int, default=1, help="Page number of results.")
    spl_parser.add_argument("--pagesize", type=int, default=5, help="Results per page (max 100).")
    spl_parser.add_argument("--application_number", type=str, help="Filter by NDA number.")
    spl_parser.add_argument("--boxed_warning", type=bool, help="Filter by boxed warning (True/False).")
    spl_parser.add_argument("--dea_schedule_code", type=str, help="Filter by DEA schedule (e.g., 'C48676' for CIII).")
    spl_parser.add_argument("--doctype", type=str, help="Filter by document type (e.g., 'C78841' for HUMAN_PRESCRIPTION_DRUG_LABEL).")
    spl_parser.add_argument("--drug_class_code", type=str, help="Filter by drug class code.")
    spl_parser.add_argument("--drug_class_coding_system", type=str, help="Coding system for drug_class_code.")
    spl_parser.add_argument("--drug_name", type=str, help="Search by drug name (e.g., 'aspirin').")
    spl_parser.add_argument("--name_type", type=str, help="Type of name (g' for generic, 'b' for brand).")
    spl_parser.add_argument("--labeler", type=str, help="Filter by labeler name.")
    spl_parser.add_argument("--manufacturer", type=str, help="Filter by manufacturer name.")
    spl_parser.add_argument("--marketing_category_code", type=str, help="Filter by marketing category (e.g., 'C73384' for NDA).")
    spl_parser.add_argument("--ndc", type=str, help="Search by NDC code.")
    spl_parser.add_argument("--published_date", type=str, help="Filter by published date (YYYY-MM-DD).")
    spl_parser.add_argument("--published_date_comparison", type=str, help="Comparison for date (lt, lte, gt, gte, eq).")
    spl_parser.add_argument("--rxcui", type=str, help="Filter by RxNorm CUI.")
    spl_parser.add_argument("--setid", type=str, help="Filter by SPL SET ID.")
    spl_parser.add_argument("--unii_code", type=str, help="Filter by UNII code.")


    # --- get-spl command ---
    get_spl_parser = subparsers.add_parser("get-spl", help="Get a specific SPL by its SET ID.")
    get_spl_parser.add_argument("set_id", type=str, help="The SET ID of the SPL.")

    # --- get-spl-history command ---
    history_parser = subparsers.add_parser("get-spl-history", help="Get the version history for an SPL.")
    history_parser.add_argument("set_id", type=str, help="The SET ID of the SPL.")

    # --- get-spl-ndcs command ---
    ndcs_parser = subparsers.add_parser("get-spl-ndcs", help="Get the NDCs for an SPL.")
    ndcs_parser.add_argument("set_id", type=str, help="The SET ID of the SPL.")
    
    # --- get-spl-packaging command ---
    pkg_parser = subparsers.add_parser("get-spl-packaging", help="Get the packaging information for an SPL.")
    pkg_parser.add_argument("set_id", type=str, help="The SET ID of the SPL.")

    # --- Listing commands (drugnames, ndcs, drugclasses, uniis) ---
    
    # get-drugnames
    drugnames_parser = subparsers.add_parser("get-drugnames", help="Get a list of all drugnames.")
    drugnames_parser.add_argument("--page", type=int, default=1, help="Page number of results.")
    drugnames_parser.add_argument("--pagesize", type=int, default=10, help="Results per page (max 100).")
    drugnames_parser.add_argument("--manufacturer", type=str, help="Filter by manufacturer name.")
    drugnames_parser.add_argument("--name_type", type=str, help="Filter by name type ('g' for generic, 'b' for brand).")

    # get-ndcs
    ndcs_list_parser = subparsers.add_parser("get-ndcs", help="Get a list of all ndcs.")
    ndcs_list_parser.add_argument("--page", type=int, default=1, help="Page number of results.")
    ndcs_list_parser.add_argument("--pagesize", type=int, default=10, help="Results per page (max 100).")
    ndcs_list_parser.add_argument("--application_number", type=str, help="Filter by NDA number.")
    ndcs_list_parser.add_argument("--labeler", type=str, help="Filter by labeler name.")
    ndcs_list_parser.add_argument("--marketing_category_code", type=str, help="Filter by marketing category.")
    ndcs_list_parser.add_argument("--setid", type=str, help="Filter by SPL SET ID.")

    # get-drugclasses
    drugclasses_parser = subparsers.add_parser("get-drugclasses", help="Get a list of all drugclasses.")
    drugclasses_parser.add_argument("--page", type=int, default=1, help="Page number of results.")
    drugclasses_parser.add_argument("--pagesize", type=int, default=10, help="Results per page (max 100).")
    drugclasses_parser.add_argument("--drug_class_code", type=str, help="Filter by drug class code.")
    drugclasses_parser.add_argument("--drug_class_coding_system", type=str, help="Coding system for drug_class_code.")
    drugclasses_parser.add_argument("--class_code_type", type=str, help="Filter by class code type (e.g., 'epc', 'moa').")
    drugclasses_parser.add_argument("--class_name", type=str, help="Filter by class name (e.g., 'opioid').")
    drugclasses_parser.add_argument("--unii_code", type=str, help="Filter by UNII code.")

    # get-uniis
    uniis_parser = subparsers.add_parser("get-uniis", help="Get a list of all uniis.")
    uniis_parser.add_argument("--page", type=int, default=1, help="Page number of results.")
    uniis_parser.add_argument("--pagesize", type=int, default=10, help="Results per page (max 100).")
    uniis_parser.add_argument("--active_moiety", type=str, help="Filter by active moiety UNII code.")
    uniis_parser.add_argument("--drug_class_code", type=str, help="Filter by drug class code.")
    uniis_parser.add_argument("--drug_class_coding_system", type=str, help="Coding system for drug_class_code.")
    uniis_parser.add_argument("--rxcui", type=str, help="Filter by RxNorm CUI.")
    uniis_parser.add_argument("--unii_code", type=str, help="Filter by UNII code.")

    # get-rxcuis
    rxcuis_parser = subparsers.add_parser("get-rxcuis", help="Get a list of all rxcuis.")
    rxcuis_parser.add_argument("--page", type=int, default=1, help="Page number of results.")
    rxcuis_parser.add_argument("--pagesize", type=int, default=10, help="Results per page (max 100).")
    rxcuis_parser.add_argument("--rxcui", type=str, help="Filter by a specific RxCUI.")
    rxcuis_parser.add_argument("--rxstring", type=str, help="Filter by a display name string (e.g., 'aspirin').")
    rxcuis_parser.add_argument("--rxtty", type=str, help="Filter by RxNorm term type (e.g., 'IN' for Ingredient).")


    args = parser.parse_args()
    api = DailyMedAPI()
    
    try:
        result = None
        if args.command == "search-spls":
            result = api.search_spls(
                page=args.page, 
                pagesize=args.pagesize,
                application_number=args.application_number,
                boxed_warning=args.boxed_warning,
                dea_schedule_code=args.dea_schedule_code,
                doctype=args.doctype,
                drug_class_code=args.drug_class_code,
                drug_class_coding_system=args.drug_class_coding_system,
                drug_name=args.drug_name,
                name_type=args.name_type,
                labeler=args.labeler,
                manufacturer=args.manufacturer,
                marketing_category_code=args.marketing_category_code,
                ndc=args.ndc,
                published_date=args.published_date,
                published_date_comparison=args.published_date_comparison,
                rxcui=args.rxcui,
                setid=args.setid,
                unii_code=args.unii_code
            )
        
        elif args.command == "get-spl":
            result = api.get_spl_by_setid(args.set_id)
            
        elif args.command == "get-spl-history":
            result = api.get_spl_history(args.set_id)
            
        elif args.command == "get-spl-ndcs":
            result = api.get_spl_ndcs(args.set_id)
            
        elif args.command == "get-spl-packaging":
            result = api.get_spl_packaging(args.set_id)
            
        elif args.command == "get-drugnames":
            result = api.get_drug_names(
                page=args.page, 
                pagesize=args.pagesize,
                manufacturer=args.manufacturer,
                name_type=args.name_type
            )
            
        elif args.command == "get-ndcs":
            result = api.get_ndcs(
                page=args.page, 
                pagesize=args.pagesize,
                application_number=args.application_number,
                labeler=args.labeler,
                marketing_category_code=args.marketing_category_code,
                setid=args.setid
            )
            
        elif args.command == "get-drugclasses":
            result = api.get_drug_classes(
                page=args.page, 
                pagesize=args.pagesize,
                drug_class_code=args.drug_class_code,
                drug_class_coding_system=args.drug_class_coding_system,
                class_code_type=args.class_code_type,
                class_name=args.class_name,
                unii_code=args.unii_code
            )
            
        elif args.command == "get-uniis":
            result = api.get_uniis(
                page=args.page, 
                pagesize=args.pagesize,
                active_moiety=args.active_moiety,
                drug_class_code=args.drug_class_code,
                drug_class_coding_system=args.drug_class_coding_system,
                rxcui=args.rxcui,
                unii_code=args.unii_code
            )
        
        elif args.command == "get-rxcuis":
            result = api.get_rxcuis(
                page=args.page,
                pagesize=args.pagesize,
                rxcui=args.rxcui,
                rxstring=args.rxstring,
                rxtty=args.rxtty
            )

        if result:
            if args.command == "get-spl":
                print("API Response (XML):")
                print(result)
            else:
                print("API Response:")
                pretty_print_json(result)

    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        print(f"\nAn error occurred during the API request: {e}", file=sys.stderr)
        print("Please check your connection and the API endpoint status.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()