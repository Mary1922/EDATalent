import io
import re
import sys
import time
import unicodedata
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup


sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

print("IMPROVED SCRAPING OF TECNOEMPLEO.COM")
print("=" * 90 + "\n")

BASE_URL = "https://www.tecnoempleo.com"
OUTPUT_FILE = "tecnoempleo_jobs_enriched.csv"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# These slugs must stay in Spanish because Tecnoempleo uses them in its URLs.
SEARCH_TERMS = [
    "big-data",
    "analista-de-datos",
    "ingeniero-de-datos",
    "cientifico-de-datos",
]


def remove_accents(text):
    normalized_text = unicodedata.normalize("NFKD", text or "")
    return "".join(
        character for character in normalized_text if not unicodedata.combining(character)
    )


def clean_text(text):
    return re.sub(r"\s+", " ", text or "").strip()


def extract_salary(text):
    match = re.search(
        r"(\d{2,3}\.?\d{3}\s*€\s*-\s*\d{2,3}\.?\d{3}\s*€(?:\s*b/a)?)",
        text,
        re.IGNORECASE,
    )
    return clean_text(match.group(1)) if match else "Not specified"


def extract_experience(text):
    normalized_text = remove_accents(text).lower()
    patterns = [
        r"(\d+)\s*(?:\+)?\s*anos?\s+de\s+experiencia",
        r"experiencia\s+(?:minima\s+)?(?:de\s+)?(\d+)\s*(?:\+)?\s*anos?",
        r"at\s+least\s+(\d+)\s*(?:\+)?\s*years",
        r"(\d+)\s*(?:\+)?\s*years?\s+of\s+experience",
    ]
    for pattern in patterns:
        match = re.search(pattern, normalized_text, re.IGNORECASE)
        if match:
            return f"{match.group(1)}+ years"
    return "Not specified"


def extract_contract_type(text):
    normalized_text = remove_accents(text).lower()
    if "indefinido" in normalized_text or "permanent" in normalized_text:
        return "Permanent"
    if "temporal" in normalized_text or "temporary" in normalized_text:
        return "Temporary"
    if "freelance" in normalized_text:
        return "Freelance"
    return "Not specified"


def extract_location_and_date(card):
    location = "Not specified"
    publication_date = "Not specified"
    desktop_meta = card.find_next_sibling("div", class_="col-12")
    mobile_meta = card.find("span", class_="d-block")

    location_element = None
    if desktop_meta:
        location_element = desktop_meta.find("b")
    if not location_element and mobile_meta:
        location_element = mobile_meta.find("b")
    if location_element:
        location = clean_text(location_element.get_text(" ", strip=True))

    meta_text = clean_text(
        desktop_meta.get_text(" ", strip=True) if desktop_meta else mobile_meta.get_text(" ", strip=True)
        if mobile_meta
        else ""
    )

    date_match = re.search(r"\d{2}/\d{2}/\d{4}", meta_text)
    if date_match:
        publication_date = date_match.group(0)

    if not location or location.lower() in {"nueva", "actualizada"}:
        location = "Not specified"

    return location, publication_date


def extract_listing_cards(soup):
    cards = []
    for card in soup.find_all("div", class_=["col-10", "col-md-9", "col-lg-7"]):
        title_link = card.select_one("h3 a[href]")
        company_link = card.select_one("a.text-primary")
        if not title_link or not company_link:
            continue

        href = title_link.get("href", "")
        if "/rf-" not in href:
            continue

        cards.append((card, title_link, company_link))
    return cards


jobs = []
seen_urls = set()
job_number = 1

for search_term in SEARCH_TERMS:
    print(f"Searching: '{search_term}'...")

    try:
        url = f"{BASE_URL}/ofertas-trabajo/{search_term}"
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        print("   Successful connection")

        soup = BeautifulSoup(response.content, "lxml")
        listing_cards = extract_listing_cards(soup)
        print(f"   Offer cards found: {len(listing_cards)}\n")

        for card, title_link, company_link in listing_cards[:30]:
            title = clean_text(title_link.get_text(" ", strip=True))
            company = clean_text(company_link.get_text(" ", strip=True))
            offer_url = urljoin(BASE_URL, title_link["href"])

            if offer_url in seen_urls:
                continue
            seen_urls.add(offer_url)

            location, publication_date = extract_location_and_date(card)
            listing_text = clean_text(card.parent.get_text(" ", strip=True))
            description_element = card.find("span", class_="hidden-md-down")
            description = clean_text(
                description_element.get_text(" ", strip=True) if description_element else ""
            )
            technologies = [
                clean_text(badge.get_text(" ", strip=True))
                for badge in card.select("span.badge.bg-gray-500")
            ]
            technology_stack = ", ".join(technologies) if technologies else "Not specified"

            salary = extract_salary(listing_text)
            experience = extract_experience(listing_text)
            contract_type = extract_contract_type(listing_text)

            if salary == "Not specified" or experience == "Not specified" or contract_type == "Not specified":
                try:
                    detail_response = requests.get(offer_url, headers=HEADERS, timeout=10)
                    if detail_response.status_code == 200:
                        detail_soup = BeautifulSoup(detail_response.content, "lxml")
                        detail_text = clean_text(detail_soup.get_text(" ", strip=True))
                        if salary == "Not specified":
                            salary = extract_salary(detail_text)
                        if experience == "Not specified":
                            experience = extract_experience(detail_text)
                        if contract_type == "Not specified":
                            contract_type = extract_contract_type(detail_text)
                except Exception:
                    pass

            jobs.append(
                {
                    "Category": search_term.replace("-", " ").title(),
                    "No": job_number,
                    "Title": title[:120],
                    "Company": company[:80],
                    "Location": location[:80],
                    "Publication Date": publication_date,
                    "Technology Stack": technology_stack[:150],
                    "Salary": salary[:80],
                    "Experience": experience,
                    "Contract Type": contract_type,
                    "URL": offer_url[:180],
                    "Description": description[:250],
                }
            )
            print(f"   [{job_number}] {title[:50]}... -> {company}")
            job_number += 1

    except Exception as error:
        print(f"   Error: {error}\n")

    time.sleep(1)

df = pd.DataFrame(jobs)

print("\n" + "=" * 90)
print("IMPROVED SCRAPING SUMMARY")
print("=" * 90)

if len(df) > 0:
    print(f"\nTotal jobs extracted: {len(df)}")
    print(f"Columns: {', '.join(df.columns.tolist())}")

    print("\nDISTRIBUTION BY CATEGORY:")
    print(df["Category"].value_counts().to_string())

    print("\nTOP 5 COMPANIES:")
    print(df["Company"].value_counts().head(5).to_string())

    print("\nTOP 5 LOCATIONS:")
    print(df["Location"].value_counts().head(5).to_string())

    print("\nMOST COMMON TECHNOLOGIES:")
    all_technologies = []
    for stack_value in df["Technology Stack"]:
        if stack_value and stack_value != "Not specified":
            all_technologies.extend([technology.strip() for technology in stack_value.split(",")])

    technology_counts = {}
    for technology in all_technologies:
        technology_counts[technology] = technology_counts.get(technology, 0) + 1

    top_technologies = sorted(
        technology_counts.items(), key=lambda item: item[1], reverse=True
    )[:10]
    for technology, count in top_technologies:
        print(f"  - {technology}: {count} offers")

    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

    print(f"\n{'=' * 90}")
    print("FILE SAVED SUCCESSFULLY")
    print(f"Name: {OUTPUT_FILE}")
    print(f"Total records: {len(df)}")
    print(f"Columns in the dataset: {len(df.columns)}")
    print(f"{'=' * 90}\n")

    print("DATA SAMPLE (first 15 records):\n")
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", None)
    pd.set_option("display.max_colwidth", 40)
    print(df.head(15).to_string(index=False))
else:
    print("\nNo jobs were extracted.")
