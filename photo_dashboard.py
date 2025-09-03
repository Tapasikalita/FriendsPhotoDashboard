import streamlit as st
from googleapiclient.discovery import build
from google.oauth2 import service_account

# ==========================
# 1. Google Drive Auth
# ==========================
def get_credentials():
    """Load Google Drive credentials from Streamlit secrets"""
    creds = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],  # loaded from secrets.toml
        scopes=["https://www.googleapis.com/auth/drive.readonly"],
    )
    return creds


def list_images(folder_id):
    """List images inside a Google Drive folder"""
    creds = get_credentials()
    service = build("drive", "v3", credentials=creds)

    results = (
        service.files()
        .list(
            q=f"'{folder_id}' in parents and mimeType contains 'image/' and trashed = false",
            fields="files(id, name, mimeType, webViewLink, webContentLink, thumbnailLink)",
        )
        .execute()
    )

    return results.get("files", [])


# ==========================
# 2. Streamlit UI
# ==========================
st.title("📸 Friends Photo Dashboard")

# 🔑 Replace with your Google Drive folder ID
FOLDER_ID = "YOUR_FOLDER_ID_HERE"

photos = list_images(FOLDER_ID)

if not photos:
    st.warning("No photos found in this folder.")
else:
    st.success(f"Found {len(photos)} photos!")

    for photo in photos:
        with st.container():
            st.image(photo["thumbnailLink"], caption=photo["name"], use_column_width=True)
            st.markdown(f"[🔗 View in Google Drive]({photo['webViewLink']})", unsafe_allow_html=True)
            st.download_button(
                label="⬇️ Download",
                data=photo["webContentLink"],
                file_name=photo["name"],
            )
