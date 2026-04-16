# TODO: los archivos .flact tiene problemas  hay que procesar los flac a wav    !!!!!


import base64
import os
from typing import Optional

import httpx
from fastapi import FastAPI, File, Form, HTTPException, UploadFile

VLLM_URL = os.getenv("VLLM_URL", "http://vllm:8080")
MODEL_NAME = "Qwen/Qwen3-ASR-0.6B"

app = FastAPI(title="Qwen3-ASR API")


@app.get("/health")
async def health():
    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            r = await client.get(f"{VLLM_URL}/health")
            vllm_ok = r.status_code == 200
        except Exception:
            vllm_ok = False
    return {"api": "ok", "vllm": "ok" if vllm_ok else "unavailable"}


@app.post("/transcribe")
async def transcribe(
    file: UploadFile = File(...),
    language: Optional[str] = Form(
        default=None,
        description="Force a specific language (e.g. 'English', 'Spanish'). Leave empty for auto-detection.",
    ),
):
    """
    Transcribes an audio file using Qwen3-ASR-1.7B.

    - **file**: audio file (wav, mp3, m4a, flac, ogg, ...)
    - **language**: optional language hint. When omitted the model auto-detects it.

    Returns `{"language": "...", "text": "..."}`.
    """
    contents = await file.read()
    if not contents:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    mime = file.content_type or "audio/wav"
    b64 = base64.b64encode(contents).decode()
    audio_url = f"data:{mime};base64,{b64}"

    content: list = [{"type": "audio_url", "audio_url": {"url": audio_url}}]
    if language:
        content.append({"type": "text", "text": f"Please transcribe in {language}."})

    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": content}],
        "max_tokens": 1024,
        "temperature": 0.0,
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            response = await client.post(f"{VLLM_URL}/v1/chat/completions", json=payload)
        except httpx.ConnectError:
            raise HTTPException(status_code=503, detail="vLLM service is unreachable")

    if response.status_code != 200:
        raise HTTPException(status_code=502, detail=f"vLLM error {response.status_code}: {response.text}")

    raw: str = response.json()["choices"][0]["message"]["content"]

    # Qwen3-ASR output format: "<lang>\n<transcription>" or plain text.
    # Try to split language tag from transcription.
    detected_language: Optional[str] = None
    text = raw.strip()
    if "\n" in text:
        first_line, rest = text.split("\n", 1)
        # Heuristic: first line is language if it has no spaces and is short
        if len(first_line) < 30 and " " not in first_line.strip():
            detected_language = first_line.strip()
            text = rest.strip()

    return {"language": detected_language, "text": text, "raw": raw}
