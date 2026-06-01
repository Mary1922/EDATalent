import pandas as pd


DATASET_FILE = "empleos_tecnoempleo.csv"
CANONICAL_COLUMNS = [
    "Category",
    "No",
    "Title",
    "Company",
    "Location",
    "Technology Stack",
    "Salary",
    "Experience",
    "Contract Type",
    "URL",
]

df = pd.read_csv(DATASET_FILE)
if list(df.columns) != CANONICAL_COLUMNS and len(df.columns) == len(CANONICAL_COLUMNS):
    df.columns = CANONICAL_COLUMNS

print("\n")
print("=" * 100)
print("DATASET COMPLETED - SCRAPING FROM TECNOEMPLEO.COM".center(100))
print("=" * 100)
print()

print("DATASET SUMMARY:")
print("-" * 100)
print(f"  File: {DATASET_FILE}")
print(f"  Total jobs: {len(df)} records")
print(f"  Columns: {len(df.columns)} fields of information")
print()

print("DATASET COLUMNS:")
print("-" * 100)
columns = {
    "Category": "Search type (Big Data / Analyst / Engineer / Data Scientist)",
    "No": "Record number",
    "Title": "Job title",
    "Company": "Company posting the offer",
    "Location": "Location (Madrid, Barcelona, remote, etc.)",
    "Technology Stack": "Required technologies (Python, SQL, Azure, AWS, etc.)",
    "Salary": "Salary range",
    "Experience": "Years of experience required",
    "Contract Type": "Contract type (Permanent, Temporary, etc.)",
    "URL": "Link to the full offer",
}

for index, (column, description) in enumerate(columns.items(), 1):
    print(f"  {index:2}. {column:20} -> {description}")
print()

print("DISTRIBUTION BY CATEGORY:")
print("-" * 100)
for category, count in df["Category"].value_counts().items():
    percentage = (count / len(df)) * 100
    bar = "#" * int(percentage / 5)
    print(f"  - {category:20} {count:3} jobs [{bar:<20}] {percentage:5.1f}%")
print()

print("DISTRIBUTION BY LOCATION:")
print("-" * 100)
for location, count in df["Location"].value_counts().head(10).items():
    percentage = (count / len(df)) * 100
    print(f"  - {location:30} {count:3} jobs ({percentage:5.1f}%)")
print()

print("MOST REQUIRED TECHNOLOGY STACK:")
print("-" * 100)
technology_counts = {}
for stack in df["Technology Stack"]:
    if stack and stack != "Not specified":
        for technology in stack.split(","):
            technology = technology.strip()
            technology_counts[technology] = technology_counts.get(technology, 0) + 1

top_technologies = sorted(
    technology_counts.items(), key=lambda item: item[1], reverse=True
)[:15]
for index, (technology, count) in enumerate(top_technologies, 1):
    percentage = (count / len(df)) * 100
    bar = "#" * int(count / 4)
    print(f"  {index:2}. {technology:15} {count:2} jobs {bar:<20} ({percentage:5.1f}%)")
print()

print("EXAMPLES OF EXTRACTED JOBS:")
print("-" * 100)
for _, row in df.head(3).iterrows():
    print()
    print(f"  Job No. {row['No']}")
    print(f"  {row['Category']} -> {row['Title']}")
    print(f"  Company: {row['Company']}")
    print(f"  Location: {row['Location']}")
    print(f"  Technology stack: {row['Technology Stack']}")
    print(f"  Contract type: {row['Contract Type']}")
    print(f"  Experience: {row['Experience']}")
    print(f"  URL: {row['URL'][:70]}...")
    print()

print("-" * 100)
print("Dataset ready for analysis and processing")
