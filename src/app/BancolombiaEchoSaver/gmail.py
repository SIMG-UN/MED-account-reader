import base64
import pickle
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from src import settings

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

credentials_path = settings.ROOT / "data" / "credentials.json"
token_path = settings.ROOT / "data" / "token.pickle"


def get_credentials():
    creds = None

    if token_path.exists():
        with open(token_path, "rb") as f:
            creds = pickle.load(f)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(credentials_path),
                SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open(token_path, "wb") as f:
            pickle.dump(creds, f)

    return creds


def extract_body(payload):
    if "body" in payload and payload["body"].get("data"):
        return base64.urlsafe_b64decode(
            payload["body"]["data"]
        ).decode("utf-8", errors="replace")

    if "parts" in payload:
        for part in payload["parts"]:
            if part.get("mimeType") == "text/plain":
                if part["body"].get("data"):
                    return base64.urlsafe_b64decode(
                        part["body"]["data"]
                    ).decode("utf-8", errors="replace")

    return ""


def get_all_messages(service, query):

    messages = []
    request = service.users().messages().list(
        userId="me",
        q=query,
        maxResults=500
    )

    while request is not None:
        response = request.execute()
        messages.extend(response.get("messages", []))

        request = service.users().messages().list_next(
            previous_request=request,
            previous_response=response
        )

    return messages


def fetch_message(service, msg_id):

    msg = service.users().messages().get(
        userId="me",
        id=msg_id,
        format="full"
    ).execute()

    headers = msg["payload"]["headers"]

    header_dict = {h["name"]: h["value"] for h in headers}

    body = extract_body(msg["payload"])

    return {
        "id": msg_id,
        "from": header_dict.get("From"),
        "to": header_dict.get("To"),
        "subject": header_dict.get("Subject"),
        "date": header_dict.get("Date"),
        "body": body
    }


def main():

    creds = get_credentials()

    service = build(
        "gmail",
        "v1",
        credentials=creds
    )
    profile = service.users().getProfile(userId="me").execute()
    print("Email autenticado:", profile["emailAddress"])

    query = "alertasynotificaciones@an.notificacionesbancolombia.com" #

    messages = get_all_messages(service, query)

    print("Total encontrados:", len(messages))

    emails = []

    for m in messages:
        emails.append(fetch_message(service, m["id"]))

    import json

    output_path = settings.ROOT / "data" / "bancolombia.json"

    with open(output_path, "w") as f:
        json.dump(emails, f, indent=2)

    print("Guardado en:", output_path)


if __name__ == "__main__":
    main()


"""
python3 -m src.app.BancolombiaEchoSaver.gmail  information_structurer

"""