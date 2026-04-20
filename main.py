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
# Helpers
# ----------------------------
def normalize_site(site):
    """
    Convert F024 -> F24, leave other formats unchanged
    """
    site = site.strip()
    if site.startswith("F0") and len(site) == 4:
        return "F" + site[2:]
    return site

# ----------------------------
# Read JSL template
# ----------------------------
jsl_text = JSL_TEMPLATE.read_text()

parameter_lines = []
site = None
tech = None

# ----------------------------
# Read CSV and build Parameters
# ----------------------------
with open(CSV_FILE, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:
        parameter_lines.append(
            f'/COLLECTION_NAME="{row["Collection Name"]}" '
            f'/WINDOW="{row["Window"]}" '
            f'/VARIABLE="{row["Variable"]}" '
            f'/STATISTIC="{row["Statistic"]}" '
            f'/CONTEXT_GROUP="{row["Context Group"]}"'
        )

        # Capture Site / Technology from first row
        if site is None:
            site = normalize_site(row.get("Facility", ""))
        if tech is None:
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
# Replace Site / Technology
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