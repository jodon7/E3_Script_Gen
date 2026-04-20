import csv
import re
import html
from pathlib import Path


def normalize_site(site: str) -> str:
    site = site.strip()
    if site.startswith("F0") and len(site) == 4:
        return "F" + site[2:]
    return site


def normalize_headers(row: dict) -> dict:
    """
    Normalize CSV headers:
      - strip whitespace
      - lowercase
      - replace underscores with spaces
    """
    return {
        key.strip().lower().replace("_", " "): value
        for key, value in row.items()
    }


def generate_jsl(csv_file: Path, template_file: Path, output_file: Path):
    # ------------------------------------------------------------------
    # 1. Read template and unescape HTML entities (fixes &amp;lt; issues)
    # ------------------------------------------------------------------
    jsl_text = html.unescape(template_file.read_text(encoding="utf-8"))

    parameter_lines = []
    site = None
    tech = None

    # ------------------------------------------------------------------
    # 2. Read CSV and build parameters
    # ------------------------------------------------------------------
    with open(csv_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        print("CSV headers found:", reader.fieldnames)

        for raw_row in reader:
            row = normalize_headers(raw_row)

            parameter_lines.append(
                f'/COLLECTION_NAME="{row["collection name"]}" '
                f'/WINDOW="{row["window"]}" '
                f'/VARIABLE="{row["variable"]}" '
                f'/STATISTIC="{row["statistic"]}" '
                f'/CONTEXT_GROUP="{row["context group"]}"'
            )

            if site is None and row.get("facility"):
                site = normalize_site(row["facility"])

            if tech is None and row.get("process"):
                tech = row["process"].strip()

    print("Parameters generated:", len(parameter_lines))

    if not parameter_lines:
        raise ValueError(
            "No parameters were generated.\n"
            "Check CSV headers and ensure the file has data rows."
        )

    new_parameters = "\n".join(parameter_lines)

    # ------------------------------------------------------------------
    # 3. Inject Parameters (NOTE: tags are REAL <Parameters> now)
    # ------------------------------------------------------------------
    jsl_text = re.sub(
        r"<Parameters>\s*</Parameters>",
        f"<Parameters>{new_parameters}</Parameters>",
        jsl_text,
        flags=re.DOTALL,
    )

    # ------------------------------------------------------------------
    # 4. Inject Site and Technology
    # ------------------------------------------------------------------
    if site:
        jsl_text = re.sub(
            r"<Site>.*?</Site>",
            f"<Site>{site}</Site>",
            jsl_text,
            flags=re.DOTALL,
        )

    if tech:
        jsl_text = re.sub(
            r"<Technology>.*?</Technology>",
            f"<Technology>{tech}</Technology>",
            jsl_text,
            flags=re.DOTALL,
        )

    # ------------------------------------------------------------------
    # 5. Final safety checks
    # ------------------------------------------------------------------
    if "<Parameters></Parameters>" in jsl_text:
        raise RuntimeError("Parameters block was not populated.")

    if "&amp;lt;" in jsl_text:
        raise RuntimeError("HTML-escaped XML detected in output.")

    # ------------------------------------------------------------------
    # 6. Write output
    # ------------------------------------------------------------------
    output_file.write_text(jsl_text, encoding="utf-8")
