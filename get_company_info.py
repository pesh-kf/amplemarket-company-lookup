import os
import requests
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

AMPLEMARKET_API_KEY = os.getenv("AMPLEMARKET_API_KEY")

def fetch_company_data(company_input):
    """
    Fetches company data from the Amplemarket API.
    """
    if not AMPLEMARKET_API_KEY:
        print("Error: AMPLEMARKET_API_KEY not found in .env file or environment variables.")
        return None

    headers = {
        "Authorization": f"Bearer {AMPLEMARKET_API_KEY}"
    }

    # Determine if the input is a LinkedIn URL or a domain
    trimmed_input = company_input.strip()
    api_url_base = "https://api.amplemarket.com/companies/find"

    if "linkedin.com/company/" in trimmed_input:
        params = {"linkedin_url": trimmed_input}
    else:
        # Assume it's a domain. More robust parsing might be needed for complex inputs.
        domain = trimmed_input
        if domain.startswith("http://"):
            domain = domain[7:]
        if domain.startswith("https://"):
            domain = domain[8:]
        if "/" in domain:
            domain = domain.split('/')[0]
        params = {"domain": domain}

    try:
        response = requests.get(api_url_base, headers=headers, params=params)
        response.raise_for_status() # Will raise an HTTPError for bad responses (4XX or 5XX)

        return response.json() # Returns the parsed JSON data

    except requests.exceptions.HTTPError as errh:
        if response.status_code == 404:
            print(f"Error: Company not found for '{company_input}'. (404)")
        else:
            print(f"HTTP Error: {errh}")
            print(f"Response Content: {response.text}") # Show more details for other HTTP errors
        return None
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
        return None
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
        return None
    except requests.exceptions.RequestException as err:
        print(f"An Unexpected Error Occurred: {err}")
        return None
    except json.JSONDecodeError:
        print("Error: Could not decode JSON response from API.")
        print(f"Response Content: {response.text}")
        return None


if __name__ == "__main__":
    print("Amplemarket Company Data Fetcher")
    print("--------------------------------")

    company_url_input = input("Enter company website domain or LinkedIn URL: ")

    if not company_url_input:
        print("No input provided. Exiting.")
    else:
        data = fetch_company_data(company_url_input)

        if data:
            print("\n--- Company Data ---")
            print(f"Name: {data.get('name', 'N/A')}")
            print(f"Website: {data.get('website', 'N/A')}")

            technologies = data.get('technologies', [])
            if technologies:
                print("Technologies:")
                for tech in technologies:
                    print(f"  - {tech}")
            else:
                print("Technologies: N/A or none listed")

            # You can print more fields from the 'data' dictionary if needed
            # print("\n--- Raw Data (for debugging) ---")
            # print(json.dumps(data, indent=2))
        else:
            print("\nNo data retrieved.")