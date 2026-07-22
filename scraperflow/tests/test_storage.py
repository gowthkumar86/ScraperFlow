# tests/test_storage.py
import json
from scraperflow.storage import save_records


def test_save_records_creates_valid_json(tmp_path):
    records = [
        {"url": "http://example.com/1", "title": "Book One", "price": "£10.00"},
        {"url": "http://example.com/2", "title": "Book Two", "price": "£20.00"},
    ]
    output_file = tmp_path / "output.json"

    save_records(records, str(output_file))

    loaded = json.loads(output_file.read_text(encoding="utf-8"))
    assert loaded == records


def test_save_records_overwrites_existing_file(tmp_path):
    output_file = tmp_path / "output.json"
    output_file.write_text('[{"old": "data"}]', encoding="utf-8")

    new_records = [{"url": "http://example.com/new", "title": "New Book"}]
    save_records(new_records, str(output_file))

    loaded = json.loads(output_file.read_text(encoding="utf-8"))
    assert loaded == new_records
    assert {"old": "data"} not in loaded