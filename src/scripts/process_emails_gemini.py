"""
Script para procesar correos financieros de Bancolombia con Gemini
y almacenarlos en la base de datos PostgreSQL.

Uso:
    python src/scripts/process_emails_gemini.py

Variables de entorno (via .env):
    GOOGLE_API_KEY  - API key de Google AI Studio
    DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
"""

import json
import os
import sys
import traceback
from pathlib import Path

import psycopg2
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Configuracion
# ---------------------------------------------------------------------------

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "dbname": os.getenv("DB_NAME", "local"),
    "user": os.getenv("DB_USER", "admin"),
    "password": os.getenv("DB_PASSWORD", "admin"),
}

EMAILS_DIR = Path(__file__).parent / "emails"

DEFAULT_USER = {
    "first_name": "Juan",
    "last_name": "Perez",
    "email": "juan.perez@gmail.com",
}

GEMINI_MODEL = "gemini-flash-latest"

EXPENSE_SCHEMA = {
    "type": "object",
    "properties": {
        "title":          {"type": "string"},
        "description":    {"type": "string"},
        "total_amount":   {"type": "number"},
        "currency":       {"type": "string"},
        "category":       {"type": "string", "enum": ["alimentacion", "transporte", "servicios", "transferencia", "retiro", "entretenimiento", "salud", "educacion", "otro"]},
        "merchant":       {"type": "string"},
        "type":           {"type": "string", "enum": ["personal", "negocio"]},
        "payment_method": {"type": "string", "enum": ["tarjeta_credito", "tarjeta_debito", "transferencia", "cajero", "app"]},
        "expense_date":   {"type": "string"},
        "ai_notes":       {"type": "string"},
    },
    "required": ["title", "description", "total_amount", "currency", "category", "type", "payment_method", "expense_date", "ai_notes"],
}

EXTRACTION_PROMPT = """
Eres un asistente experto en analizar correos de notificaciones bancarias colombianas.
Analiza el siguiente correo de Bancolombia y extrae la informacion financiera.

- total_amount debe ser un numero decimal sin simbolos de moneda ni puntos de miles (ej: 67500.00)
- expense_date debe inferirse de la fecha del correo en formato YYYY-MM-DD HH:MM:SS
- category e inferirse del tipo de transaccion y el comercio
- ai_notes debe incluir si el gasto es inusual, recurrente, o cualquier insight util

Correo:
---
{email_body}
---
"""

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)


def get_or_create_user(conn, user_data: dict) -> str:
    """Retorna el UUID del usuario, creandolo si no existe."""
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO users (first_name, last_name, email)
            VALUES (%s, %s, %s)
            ON CONFLICT (email) DO UPDATE
                SET first_name = EXCLUDED.first_name,
                    last_name  = EXCLUDED.last_name
            RETURNING id
            """,
            (user_data["first_name"], user_data["last_name"], user_data["email"]),
        )
        user_id = str(cur.fetchone()[0])
        conn.commit()
        return user_id



def extract_with_gemini(model, email_body: str) -> dict:
    """Usa Gemini para extraer datos financieros del correo."""
    prompt = EXTRACTION_PROMPT.format(email_body=email_body)
    return json.loads(model.generate_content(prompt).text)


def insert_expense(conn, user_id: str, data: dict) -> str:
    """Inserta un gasto en la tabla expenses y retorna el UUID."""
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO expenses (
                user_id, title, description, total_amount, currency,
                category, merchant, type, payment_method, expense_date, ai_notes
            ) VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s
            )
            RETURNING id
            """,
            (
                user_id,
                data["title"],
                data["description"],
                data["total_amount"],
                data["currency"],
                data["category"],
                data.get("merchant"),
                data["type"],
                data["payment_method"],
                data["expense_date"],
                data["ai_notes"],
            ),
        )
        expense_id = str(cur.fetchone()[0])
        conn.commit()
        return expense_id


def main():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("ERROR: La variable de entorno GOOGLE_API_KEY no esta definida.")
        print("       Obten tu API key en: https://aistudio.google.com/app/apikey")
        sys.exit(1)

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        GEMINI_MODEL,
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json",
            response_schema=EXPENSE_SCHEMA,
        ),
    )
    print(f"Modelo Gemini: {GEMINI_MODEL}")

    print("Conectando a PostgreSQL...")
    try:
        conn = get_db_connection()
        print("  Conexion exitosa.")
    except Exception as e:
        print(f"ERROR conectando a la DB: {e}")
        sys.exit(1)

    try:
        user_id = get_or_create_user(conn, DEFAULT_USER)
        print(f"  Usuario activo: {DEFAULT_USER['email']} (id: {user_id})\n")

        email_files = sorted(EMAILS_DIR.glob("*.eml"))
        if not email_files:
            print(f"No se encontraron archivos .eml en {EMAILS_DIR}")
            sys.exit(0)

        print(f"Procesando {len(email_files)} correo(s) en {EMAILS_DIR}\n")
        print("=" * 65)

        results = {"success": 0, "failed": 0}

        for filepath in email_files:
            print(f"\nArchivo : {filepath.name}")

            try:
                raw = filepath.read_text(encoding="utf-8")

                print("  Enviando a Gemini para analisis...")
                extracted = extract_with_gemini(model, raw)

                print(f"  Comercio    : {extracted.get('merchant', 'N/A')}")
                print(f"  Monto       : {extracted.get('total_amount')} {extracted.get('currency', 'COP')}")
                print(f"  Categoria   : {extracted.get('category')}")
                print(f"  Metodo pago : {extracted.get('payment_method')}")
                print(f"  Fecha       : {extracted.get('expense_date')}")

                expense_id = insert_expense(conn, user_id, extracted)
                print(f"  [DB] Gasto insertado con id: {expense_id}")
                results["success"] += 1

            except Exception:
                traceback.print_exc()
                results["failed"] += 1

        print("\n" + "=" * 65)
        print(f"Resumen: {results['success']} insertados, {results['failed']} fallidos.")

    finally:
        conn.close()


if __name__ == "__main__":
    main()
