import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

# ================================
# 1. Load credentials
# ================================
def get_credentials():
    try:
        # Case 1: Running on Streamlit Cloud → load from secrets
        if "gcp_service_account" in st.secrets:
            creds = service_account.Credentials.from_service_account_info(
                st.secrets["gcp_service_account"],
                scopes=["https://www.googleapis.com/auth/drive.readonly"],
            )
            st.sidebar.success("✅ Loaded credentials from secrets.toml")
            return creds

        # Case 2: Running locally → load from JSON file
        elif os.path.exists("service_account.json"):
            creds = service_account.Credentials.from_service_account_file(
                "service_account.json",
                scopes=["https://www.googleapis.com/auth/drive.readonly"],
            )
            st.sidebar.success("✅ Loaded credentials from service_account.json")
            return creds

        else:
            st.sidebar.error("❌ No credentials found. Please add service_account.json or secrets.toml")
            return None
    except Exception as e:
        st.sidebar.error(f"⚠️ Credential load error: {e}")
        return None


# ================================
# 2. List images from Google Drive
# ================================
def list_images(folder_id):
    creds = get_credentials()
    if creds is None:
        return []

    try:
        service = build("drive", "v3", credentials=creds)
        results = (
            service.files()
            .list(
                q=f"'{folder_id}' in parents and mimeType contains 'image/' and trashed=false",
                pageSize=50,
                fields="files(id, name, mimeType, webViewLink)",
            )
            .execute()
        )
        return results.get("files", [])
    except Exception as e:
        st.error(f"❌ Error fetching images: {e}")
        return []


# ================================
# 3. Streamlit UI
# ================================
st.set_page_config(page_title="📸 Friends Photo Dashboard", layout="wide")
st.title("📸 Friends Photo Dashboard")

st.markdown("""
Welcome to your **Group Photo Dashboard**! 🎉  

**How it works:**  
1. Upload your photos into the shared Google Drive folder.  
2. This dashboard automatically shows all uploaded photos.  
3. Click any photo to open/download it in full size.  

⚡ *No need to merge files — just drop them in Drive and they appear here.*
""")

# Put your Google Drive Folder ID here
FOLDER_ID = "1W7ecBMXSIHGVEEKZIkYqFZmHGx3miHk5"

photos = list_images(FOLDER_ID)

if photos:
    st.success(f"✅ Found {len(photos)} photos in Drive")

    for photo in photos:
        # Use direct "uc?id=" link for images
        img_url = f"https://drive.google.com/uc?id={photo['id']}"
        st.image(img_url, caption=photo["name"], use_container_width=True)
        st.markdown(f"[🔗 Open in Google Drive]({photo['webViewLink']})")
else:
    st.warning("⚠️ No photos found in the folder. Make sure the folder is shared with your service account.")
