import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

# -----------------------------
# CONFIGURATION
# -----------------------------
FOLDER_ID = "1W7ecBMXSIHGVEEKZIkYqFZmHGx3miHk5"  # replace with your folder ID

# Load credentials from local JSON file
creds = service_account.Credentials.from_service_account_file(
    "service_account.json",  # JSON file in same folder
    scopes=["https://www.googleapis.com/auth/drive.readonly"],
)

# Connect to Google Drive API
service = build("drive", "v3", credentials=creds)

def list_images(folder_id):
    """List image files from Google Drive folder"""
    results = service.files().list(
        q=f"'{folder_id}' in parents and mimeType contains 'image/' and trashed=false",
        fields="files(id, name, mimeType, webViewLink, webContentLink)"
    ).execute()
    return results.get("files", [])

# -----------------------------
# STREAMLIT APP
# -----------------------------
st.set_page_config(page_title="📸 Friends Photo Dashboard", layout="wide")
st.title("📸 Friends Photo Dashboard")

st.markdown("""
Upload your photos into the shared **Google Drive folder** 📂.  
They will appear below automatically for download or viewing.
""")

# Fetch photos
photos = list_images(FOLDER_ID)

if not photos:
    st.warning("⚠️ No photos found in the folder yet. Upload some!")
else:
    for photo in photos:
        st.image(photo["webContentLink"], caption=photo["name"], use_column_width=True)
        st.markdown(f"[📥 Download]({photo['webContentLink']})")

