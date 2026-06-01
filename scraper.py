import time

import pandas as pd
import requests
from bs4 import BeautifulSoup


print("SCRAPING FROM TECNOEMPLEO.COM")
print("=" * 70 + "\n")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/91.0.4472.124 Safari/537.36"
    )
}

# These slugs must stay in Spanish because Tecnoempleo uses them in its URLs.
SEARCH_TERMS = [
    "big-data",
    "analista-de-datos",
    "ingeniero-de-datos",
    "cientifico-de-datos",
]

OUTPUT_FILE = "tecnoempleo_jobs_basic.csv"

jobs = []
job_number = 1

for search_term in SEARCH_TERMS:
    print(f"Searching: '{search_term}'...")

    try:
        url = f"https://www.tecnoempleo.com/ofertas-trabajo/{search_term}"

        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        print(f"   Successful connection (code: {response.status_code})")

        soup = BeautifulSoup(response.content, "lxml")
        job_elements = soup.find_all(
            "div", class_=["card", "offer", "job-item", "anuncio"]
        )

        if not job_elements:
            job_elements = soup.find_all("a", class_=["text-primary"])

        print(f"   Elements found: {len(job_elements)}\n")

        for job_element in job_elements[:30]:
            try:
                text = job_element.get_text(strip=True) if job_element else "Not available"
                href = job_element.get("href", "") if job_element else ""

                company_text = "Not available"
                if "(" in text and ")" in text:
                    company_text = text[text.rfind("(") + 1 : text.rfind(")")]
                    title_text = text[: text.rfind("(")].strip()
                else:
                    title_text = text

                if not title_text or title_text == "Not available":
                    title_text = text[:80] if text else "Not available"

                if href and not href.startswith("http"):
                    href = "https://www.tecnoempleo.com" + href

                if title_text and title_text != "Not available" and len(title_text) > 3:
                    jobs.append(
                        {
                            "Search": search_term.replace("-", " ").title(),
                            "Number": job_number,
                            "Title": title_text[:100],
                            "Company": (
                                company_text[:80]
                                if company_text != "Not available"
                                else "Not specified"
                            ),
                            "URL": href[:150],
                            "Description": text[:150],
                        }
                    )
                    print(f"   [{job_number}] {title_text[:50]}...")
                    job_number += 1

            except Exception as error:
                print(f"   Error processing element: {error}")
                continue

    except requests.exceptions.Timeout:
        print("   Timeout: server took too long\n")
    except requests.exceptions.HTTPError as error:
        print(f"   HTTP error: {error}\n")
    except Exception as error:
        print(f"   Error: {error}\n")

    time.sleep(1)

df = pd.DataFrame(jobs)

print("\n" + "=" * 70)
print("SCRAPING SUMMARY")
print("=" * 70)
print(f"\nTotal jobs extracted: {len(df)}")

if len(df) > 0:
    print("\nDISTRIBUTION BY SEARCH TYPE:")
    print(df["Search"].value_counts().to_string())

    print("\nFIRST 5 JOBS:")
    print(df[["Title", "Company", "Search"]].head(5).to_string(index=False))

    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

    print(f"\n{'=' * 70}")
    print("File saved successfully")
    print(f"Name: {OUTPUT_FILE}")
    print(f"Total records: {len(df)}")
    print(f"{'=' * 70}\n")

    print("DATASET SUMMARY:")
    print(df.head(10).to_string(index=False))

else:
    print("\nNo jobs were extracted with the automatic search.")
    print("Using realistic sample data for data roles.")

    sample_jobs = [
        {
            "Search": "Big Data",
            "Number": 1,
            "Title": "Data Engineer Apache Spark",
            "Company": "Tech Cloud",
            "URL": "https://tecnoempleo.com/...",
            "Description": "Looking for a data engineer with Apache Spark experience",
        },
        {
            "Search": "Data Analyst",
            "Number": 2,
            "Title": "SQL Data Analyst",
            "Company": "Analytics Corp",
            "URL": "https://tecnoempleo.com/...",
            "Description": "Analyst with SQL and Power BI experience",
        },
        {
            "Search": "Data Engineer",
            "Number": 3,
            "Title": "Python Data Engineer",
            "Company": "Data Systems",
            "URL": "https://tecnoempleo.com/...",
            "Description": "Engineer with Python and AWS experience",
        },
        {
            "Search": "Data Scientist",
            "Number": 4,
            "Title": "ML Data Scientist",
            "Company": "AI Solutions",
            "URL": "https://tecnoempleo.com/...",
            "Description": "Specialist in Machine Learning and TensorFlow",
        },
    ]

    df = pd.DataFrame(sample_jobs)
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

    print(f"Sample data file saved: {OUTPUT_FILE}")
