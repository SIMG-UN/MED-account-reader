import json
from pathlib import Path

import httpx

API_URL = "http://localhost:8088"
IMAGE_PATH = Path(__file__).parent / "factu.jpeg"

# Optional: set an extraction schema to get structured JSON back.
# Set to None to use plain text recognition instead.
# EXTRACTION_SCHEMA = {
#     "invoice_number": "",
#     "date": "",
#     "total": "",
#     "vendor": "",
# }

EXTRACTION_SCHEMA = None

def test_health() -> None:
    response = httpx.get(f"{API_URL}/health", timeout=10.0)
    response.raise_for_status()
    print("Health:", response.json())


def test_ocr() -> None:
    with IMAGE_PATH.open("rb") as f:
        files = {"file": ("factu.jpeg", f, "image/jpeg")}
        data: dict = {}

        if EXTRACTION_SCHEMA is not None:
            data["extraction_schema"] = json.dumps(EXTRACTION_SCHEMA)
        else:
            data["task"] = "text"

        response = httpx.post(
            f"{API_URL}/ocr",
            files=files,
            data=data,
            timeout=120.0,
        )

    response.raise_for_status()
    result = response.json()
    print("OCR output:\n", result["output"])


if __name__ == "__main__":
    test_health()
    test_ocr()
