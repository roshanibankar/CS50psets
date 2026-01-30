import sys
import requests
import os
from dotenv import load_dotenv  

load_dotenv()

def main():
    if len(sys.argv) != 2:
        sys.exit("Missing command-line argument")

    try:
        n = float(sys.argv[1])
    except ValueError:
        sys.exit("Command-line argument is not a number")

    api_key = os.getenv("COINCAP_API_KEY")
    if not api_key:
        sys.exit("API key not found in environment variables")

    url = "https://rest.coincap.io/v3/assets/bitcoin"
    headers = {
        "Authorization": f"Bearer {api_key}"  
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException:
        sys.exit("Error fetching data from CoinCap API")

    try:
        data = response.json()
        price = float(data["data"]["priceUsd"])
    except (KeyError, TypeError, ValueError):
        sys.exit("Error parsing JSON response")

    total = n * price
    print(f"${total:,.4f}")

if __name__ == "__main__":
    main()
