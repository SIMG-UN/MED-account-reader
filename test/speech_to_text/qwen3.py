
from pathlib import Path

import httpx

API_URL = "http://localhost:8089"
AUDIO_PATH = Path(__file__).parent / "Recording 1.flac"


def test_health() -> None:
    response = httpx.get(f"{API_URL}/health", timeout=10.0)
    response.raise_for_status()
    print("Health:", response.json())


def test_transcribe() -> None:
    with AUDIO_PATH.open("rb") as f:
        files = {"file": ("Recording 1.flac", f, "audio/flac")}
        response = httpx.post(
            f"{API_URL}/transcribe",
            files=files,
            timeout=120.0,
        )

    response.raise_for_status()
    result = response.json()
    print("Language:", result["language"])
    print("Text:    ", result["text"])


if __name__ == "__main__":
    test_health()
    test_transcribe()
