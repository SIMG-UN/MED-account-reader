import base64
import json
import os
from typing import Optional

import httpx
from fastapi import FastAPI, File, Form, HTTPException, UploadFile

VLLM_URL = os.getenv("VLLM_URL", "http://vllm:8080")
MODEL_NAME = "zai-org/GLM-OCR"

TASK_PROMPTS = {
    "text": "Text Recognition:",
    "formula": "Formula Recognition:",
    "table": "Table Recognition:",
}

app = FastAPI(title="GLM-OCR API")


@app.get("/health")
async def health():
    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            r = await client.get(f"{VLLM_URL}/health")
            vllm_ok = r.status_code == 200
        except Exception:
            vllm_ok = False
    return {"api": "ok", "vllm": "ok" if vllm_ok else "unavailable"}


@app.post("/ocr")
async def ocr(
    file: UploadFile = File(...),
    task: str = Form(default="text", description="text | formula | table"),
    extraction_schema: Optional[str] = Form(
        default=None,
        description="JSON string with the schema for information extraction. Overrides 'task' when provided.",
    ),
):
    """
    Sends an image to GLM-OCR and returns the recognized text.

    - **task**: one of `text`, `formula`, `table` (default: `text`)
    - **extraction_schema**: optional JSON string describing fields to extract.
      When provided, the model returns a JSON object following that schema.

    Example extraction_schema:
        {"invoice_number": "", "total": "", "date": ""}
    """
    contents = await file.read()
    if not contents:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    b64 = base64.b64encode(contents).decode()
    mime = file.content_type or "image/jpeg"

    if extraction_schema is not None:
        try:
            schema = json.loads(extraction_schema)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="extraction_schema is not valid JSON")
        prompt = "请按下列JSON格式输出图中信息:\n" + json.dumps(schema, ensure_ascii=False, indent=2)
    else:
        prompt = TASK_PROMPTS.get(task, TASK_PROMPTS["text"])

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:{mime};base64,{b64}"},
                    },
                    {"type": "text", "text": prompt},
                ],
            }
        ],
        "max_tokens": 2048,
        "temperature": 0.0,
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            response = await client.post(f"{VLLM_URL}/v1/chat/completions", json=payload)
        except httpx.ConnectError:
            raise HTTPException(status_code=503, detail="vLLM service is unreachable")

    if response.status_code != 200:
        raise HTTPException(status_code=502, detail=f"vLLM error {response.status_code}: {response.text}")

    result = response.json()
    output = result["choices"][0]["message"]["content"]
    return {"output": output}
