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

    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Union[Dict[str, Any], str]:
        """
        Internal helper method to make a GET request to the DailyMed API.

        Args:
            endpoint: The API endpoint to call (e.g., "spls.json").
            params: A dictionary of query parameters for the request.

        Returns:
            A dictionary parsed from the JSON response.
            
        Raises:
            requests.exceptions.HTTPError: If the API returns an error status code.
            requests.exceptions.RequestException: For other network or request-related issues.
            json.JSONDecodeError: If the response is not valid JSON.
        """
        if params is None:
            params = {}
            
        # Ensure pagesize is reasonable if not provided
        # --- REMOVED ---
        # params.setdefault('pagesize', 10) 
        # --- This was the bug. It should only be set on paginated endpoints. ---
        
        url = f"{self.BASE_URL}/{endpoint}"
        
        try:
            response = requests.get(url, params=params, timeout=10)
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

    def search_spls(self, drug_name: Optional[str] = None, ndc: Optional[str] = None, page: int = 1, pagesize: int = 10) -> Dict[str, Any]:
        """
        Searches for Structured Product Labeling (SPLs) documents.
        
        Args:
            drug_name: The generic or brand name of the drug.
            ndc: The National Drug Code (NDC).
            page: The page number of results to return.
            pagesize: The number of results per page.

        Returns:
            The JSON response dictionary from the API.
        """
        print(f"\nSearching SPLs (Page {page}, Size {pagesize}) with filters: drug_name={drug_name}, ndc={ndc}...")
        params = {"page": page, "pagesize": pagesize}
        if drug_name:
            params['drug_name'] = drug_name
        if ndc:
            params['ndc'] = ndc
            
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
        # This endpoint doesn't take parameters, so we pass None
        # This endpoint returns XML, not JSON
        return self._make_request(f"spls/{set_id}.xml", params=None)

    def get_spl_history(self, set_id: str) -> Dict[str, Any]:
        """
        Retrieves the version history for a specific SPL.
        
        Args:
            set_id: The SET ID of the SPL document.

        Returns:
            The JSON response dictionary from the API.
        """
        print(f"\nGetting SPL history for SET ID: {set_id}...")
        # This endpoint doesn't take parameters, so we pass None
        return self._make_request(f"spls/{set_id}/history.json", params=None)

    def get_spl_ndcs(self, set_id: str) -> Dict[str, Any]:
        """
        Retrieves all NDCs associated with a specific SPL.
        
        Args:
            set_id: The SET ID of the SPL document.

        Returns:
            The JSON response dictionary from the API.
        """
        print(f"\nGetting NDCs for SET ID: {set_id}...")
        # This endpoint doesn't take parameters, so we pass None
        return self._make_request(f"spls/{set_id}/ndcs.json", params=None)

    def get_spl_packaging(self, set_id: str) -> Dict[str, Any]:
        """
        Retrieves product packaging information for a specific SPL.
        
        Args:
            set_id: The SET ID of the SPL document.

        Returns:
            The JSON response dictionary from the API.
        """
        print(f"\nGetting packaging info for SET ID: {set_id}...")
        # This endpoint doesn't take parameters, so we pass None
        return self._make_request(f"spls/{set_id}/packaging.json", params=None)

    def get_drug_names(self, page: int = 1, pagesize: int = 10) -> Dict[str, Any]:
        """
        Retrieves a list of all drug names.
        
        Args:
            page: The page number of results to return.
            pagesize: The number of results per page.

        Returns:
            The JSON response dictionary from the API.
        """
        print(f"\nGetting drug names (Page {page}, Size {pagesize})...")
        # This paginated endpoint needs pagesize
        params = {"page": page, "pagesize": pagesize}
        return self._make_request("drugnames.json", params=params)

    def get_ndcs(self, page: int = 1, pagesize: int = 10) -> Dict[str, Any]:
        """
        Retrieves a list of all NDCs.
        
        Args:
            page: The page number of results to return.
            pagesize: The number of results per page.

        Returns:
            The JSON response dictionary from the API.
        """
        print(f"\nGetting NDCs (Page {page}, Size {pagesize})...")
        # This paginated endpoint needs pagesize
        params = {"page": page, "pagesize": pagesize}
        return self._make_request("ndcs.json", params=params)

    def get_drug_classes(self, page: int = 1, pagesize: int = 10) -> Dict[str, Any]:
        """
        Retrieves a list of all drug classes.
        
        Args:
            page: The page number of results to return.
            pagesize: The number of results per page.

        Returns:
            The JSON response dictionary from the API.
        """
        print(f"\nGetting drug classes (Page {page}, Size {pagesize})...")
        # This paginated endpoint needs pagesize
        params = {"page": page, "pagesize": pagesize}
        return self._make_request("drugclasses.json", params=params)

    def get_uniis(self, page: int = 1, pagesize: int = 10) -> Dict[str, Any]:
        """
        Retrieves a list of all Unique Ingredient Identifiers (UNIIs).
        
        Args:
            page: The page number of results to return.
            pagesize: The number of results per page.

        Returns:
            The JSON response dictionary from the API.
        """
        print(f"\nGetting UNIIs (Page {page}, Size {pagesize})...")
        # This paginated endpoint needs pagesize
        params = {"page": page, "pagesize": pagesize}
        return self._make_request("uniis.json", params=params)

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
    spl_parser.add_argument("--drug_name", type=str, help="Search by drug name (e.g., 'aspirin').")
    spl_parser.add_argument("--ndc", type=str, help="Search by NDC code.")
    spl_parser.add_argument("--page", type=int, default=1, help="Page number of results.")
    spl_parser.add_argument("--pagesize", type=int, default=5, help="Results per page (max 100).")

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
    for name in ["drugnames", "ndcs", "drugclasses", "uniis"]:
        list_parser = subparsers.add_parser(f"get-{name}", help=f"Get a list of all {name}.")
        list_parser.add_argument("--page", type=int, default=1, help="Page number of results.")
        list_parser.add_argument("--pagesize", type=int, default=10, help="Results per page (max 100).")

    args = parser.parse_args()
    api = DailyMedAPI()
    
    try:
        result = None
        if args.command == "search-spls":
            result = api.search_spls(drug_name=args.drug_name, ndc=args.ndc, page=args.page, pagesize=args.pagesize)
        
        elif args.command == "get-spl":
            result = api.get_spl_by_setid(args.set_id)
            
        elif args.command == "get-spl-history":
            result = api.get_spl_history(args.set_id)
            
        elif args.command == "get-spl-ndcs":
            result = api.get_spl_ndcs(args.set_id)
            
        elif args.command == "get-spl-packaging":
            result = api.get_spl_packaging(args.set_id)
            
        elif args.command == "get-drugnames":
            result = api.get_drug_names(page=args.page, pagesize=args.pagesize)
            
        elif args.command == "get-ndcs":
            result = api.get_ndcs(page=args.page, pagesize=args.pagesize)
            
        elif args.command == "get-drugclasses":
            result = api.get_drug_classes(page=args.page, pagesize=args.pagesize)
            
        elif args.command == "get-uniis":
            result = api.get_uniis(page=args.page, pagesize=args.pagesize)
        
        if result:
            if args.command == "get-spl":
                print("API Response (XML):")
                # Truncate the XML output to avoid flooding the terminal - REMOVED
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