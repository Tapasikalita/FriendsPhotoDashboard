import streamlit as st
from googleapiclient.discovery import build
from google.oauth2 import service_account

# -----------------------
# CONFIGURATION
# -----------------------
FOLDER_ID = "YOUR_DRIVE_FOLDER_ID"  # Replace with actual folder ID

# Load service account credentials
creds = service_account.Credentials.from_service_account_file(
    "service_account.json",  # Path to JSON key
    scopes=["https://www.googleapis.com/auth/drive.readonly"],
)

# Build Google Drive API client
drive_service = build("drive", "v3", credentials=creds)


def list_images_from_drive(folder_id):
    """Fetch image files from Google Drive folder."""
    query = f"'{folder_id}' in parents and mimeType contains 'image/'"
    results = drive_service.files().list(
        q=query, fields="files(id, name, mimeType, webContentLink, webViewLink)"
    ).execute()
    return results.get("files", [])


# -----------------------
# STREAMLIT UI
# -----------------------
st.set_page_config(page_title="📸 Friends Photo Dashboard", layout="wide")
st.title("📸 Friends Photo Dashboard")

st.markdown("""
Upload your photos into the **shared Google Drive folder**.  
This dashboard automatically shows all uploaded photos.  
Click any photo to open/download it in full size.  
""")

# Fetch and display photos
photos = list_images_from_drive(FOLDER_ID)

if not photos:
    st.warning("⚠️ No photos found in the Drive folder yet. Upload some!")
else:
    st.success(f"✅ Found {len(photos)} photos in Google Drive!")

    cols = st.columns(4)
    for idx, photo in enumerate(photos):
        col = cols[idx % 4]
        col.image(f"https://drive.google.com/uc?id={photo['id']}", caption=photo["name"], use_column_width=True)
        col.markdown(f"[📥 Download]({photo['webContentLink']})")
