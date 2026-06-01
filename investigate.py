import requests
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}
OFFER_URL = "https://www.tecnoempleo.com/globalsysinfo/re-206065"

try:
    response = requests.get(OFFER_URL, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(response.content, "lxml")

    print("=" * 70)
    print("INVESTIGATING JOB OFFER STRUCTURE")
    print("=" * 70)
    print()

    page_text = soup.get_text(separator="\n")
    lines = [line.strip() for line in page_text.split("\n") if line.strip()]

    print("FIRST 100 LINES:")
    for line_number, line in enumerate(lines[:100], 1):
        print(f"{line_number:3}. {line}")

except Exception as error:
    print(f"Error: {error}")
