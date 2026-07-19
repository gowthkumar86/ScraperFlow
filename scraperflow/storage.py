import json
from pathlib import Path

def save_records(records: list[dict], output_path: str) -> None:
    """Write records to a JSON file."""
    path = Path(output_path)
    path.write_text(
        json.dumps(records, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )