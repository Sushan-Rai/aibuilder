import os
from mcp.server.fastmcp import FastMCP
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = [
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/documents.readonly"
]

server = FastMCP(
    name="Presidio-GDocs-Engine",
    dependencies=["google-api-python-client", "google-auth-oauthlib"]
)

def get_gapi_credentials():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists("credentials.json"):
                raise FileNotFoundError(
                    "Missing 'credentials.json'. Please download it from Google Cloud Console."
                )
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds

def extract_structural_text(elements) -> str:
    text = ""
    for value in elements:
        if "paragraph" in value:
            elements = value.get("paragraph").get("elements")
            for elem in elements:
                if "textRun" in elem:
                    text += elem.get("textRun").get("content")
        elif "table" in value:
            table = value.get("table")
            for row in table.get("tableRows"):
                for cell in row.get("tableCells"):
                    text += extract_structural_text(cell.get("content"))
    return text

@server.tool()
def search_and_read_presidio_docs(semantic_query: str) -> str:
    """
    Searches Presidio's Google Workspace Drive for relevant internal documents
    and extracts their full text contents matching the semantic query terms.
    """
    try:
        creds = get_gapi_credentials()
        drive_service = build("drive", "v3", credentials=creds)
        docs_service = build("docs", "v1", credentials=creds)

        mime_type_filter = "mimeType = 'application/vnd.google-apps.document'"
        search_query = f"{mime_type_filter} and (name contains '{semantic_query}' or fullText contains '{semantic_query}')"
        
        results = drive_service.files().list(
            q=search_query,
            pageSize=3, 
            fields="files(id, name)"
        ).execute()
        
        files = results.get("files", [])
        if not files:
            return f"No Presidio Google Docs found matching: '{semantic_query}'."

        compiled_corpus = []
        for file in files:
            doc_id = file["id"]
            doc_name = file["name"]
            
            document = docs_service.documents().get(documentId=doc_id).execute()
            doc_body = document.get("body").get("content")
            parsed_text = extract_structural_text(doc_body)
            
            compiled_corpus.append(f"--- Document Name: {doc_name} ---\n{parsed_text}\n")
            
        return "\n".join(compiled_corpus)

    except HttpError as err:
        return f"Google Workspace API Error: {err}"
    except Exception as e:
        return f"Internal MCP server infrastructure error: {str(e)}"

if __name__ == "__main__":
    server.run()