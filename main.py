# This python script takes DOTS output files and generates a wijit script for easy viewing
import csv
from pathlib import Path
import re

# ----------------------------
# File paths
# ----------------------------
JSL_TEMPLATE = Path("input/fdc.jsl")
CSV_FILE = Path("input/in.csv")
OUTPUT_JSL = Path("output/fdc_combined.jsl")

# ----------------------------
# Read files
# ----------------------------
jsl_text = JSL_TEMPLATE.read_text()

parameter_lines = []

with open(CSV_FILE, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:
        line = (
            f'/COLLECTION_NAME="{row["Collection Name"]}" '
            f'/WINDOW="{row["Window"]}" '
            f'/VARIABLE="{row["Variable"]}" '
            f'/STATISTIC="{row["Statistic"]}" '
            f'/CONTEXT_GROUP="{row["Context Group"]}"'
        )
        parameter_lines.append(line)

        # Optional: overwrite Site / Technology from first row
        site = row.get("Facility", "").strip()
        tech = row.get("Process", "").strip()

# ----------------------------
# Replace <Parameters> block
# ----------------------------
new_parameters = "\n".join(parameter_lines)

jsl_text = re.sub(
    r"<Parameters>.*?</Parameters>",
    f"<Parameters>{new_parameters}</Parameters>",
    jsl_text,
    flags=re.DOTALL,
)

# ----------------------------
# Optionally replace Site / Technology
# ----------------------------
if site:
    jsl_text = re.sub(
        r"<Site>.*?</Site>",
        f"<Site>{site}</Site>",
        jsl_text,
    )

if tech:
    jsl_text = re.sub(
        r"<Technology>.*?</Technology>",
        f"<Technology>{tech}</Technology>",
        jsl_text,
    )

# ----------------------------
# Write output
# ----------------------------
OUTPUT_JSL.write_text(jsl_text)

print(f"Created combined JSL: {OUTPUT_JSL}")