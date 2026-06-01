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

print("=" * 100)
print(f"ENRICHED DATASET - {DATASET_FILE}")
print("=" * 100)
print()

print("GENERAL INFORMATION:")
print(f"  Total records: {len(df)}")
print(f"  Total columns: {len(df.columns)}")
print()

print("AVAILABLE COLUMNS:")
for index, column in enumerate(df.columns, 1):
    print(f"  {index}. {column}")
print()

print("DATASET STATISTICS:")
print(f'  - Categories: {df["Category"].nunique()} ({" / ".join(df["Category"].unique())})')
print(f'  - Unique companies: {df["Company"].nunique()}')
print(f'  - Unique locations: {df["Location"].nunique()}')
print()

print("TOP LOCATIONS:")
for location, count in df["Location"].value_counts().head(8).items():
    print(f"  - {location}: {count} jobs")
print()

print("DETECTED EXPERIENCE:")
experience_counts = df["Experience"].value_counts()
for experience, count in experience_counts.items():
    print(f"  - {experience}: {count} jobs")
print()

print("SALARIES FOUND (sample):")
print(df["Salary"].value_counts().head(5))
print()

print("=" * 100)
print("DETAILED SAMPLE (first 5 jobs):")
print("=" * 100)
for _, row in df.head(5).iterrows():
    print()
    print(f"No. {row['No']} - {row['Category']}")
    print(f"  Title: {row['Title']}")
    print(f"  Company: {row['Company']}")
    print(f"  Location: {row['Location']}")
    print(f"  Stack: {row['Technology Stack']}")
    print(f"  Salary: {row['Salary']}")
    print(f"  Experience: {row['Experience']}")
    print(f"  Contract: {row['Contract Type']}")
    print()
