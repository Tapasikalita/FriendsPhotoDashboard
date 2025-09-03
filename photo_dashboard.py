import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

# -----------------------------
# CONFIGURATION
# -----------------------------
FOLDER_ID = "1W7ecBMXSIHGVEEKZIkYqFZmHGx3miHk5"  # Google Drive folder ID

# -----------------------------
# AUTHENTICATION
# -----------------------------
def get_credentials():
    try:
        # ✅ If running on Streamlit Cloud (secrets available)
        return service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=["https://www.googleapis.com/auth/drive.readonly"],
        )
    except Exception:
        # ✅ If running locally, load from JSON file
        return service_account.Credentials.from_service_account_file(
            "service_account.json",  # <-- put JSON file in same folder
            scopes=["https://www.googleapis.com/auth/drive.readonly"],
        )

# -----------------------------
# LIST IMAGES FROM DRIVE
# -----------------------------
def list_images(folder_id):
    creds = get_credentials()
    service = build("drive", "v3", credentials=creds)

    results = (
        service.files()
        .list(
            q=f"'{folder_id}' in parents and mimeType contains 'image/'",
            fields="files(id, name, mimeType, webViewLink, thumbnailLink)"
        )
        .execute()
    )
    return results.get("files", [])

# -----------------------------
# STREAMLIT APP
# -----------------------------
st.set_page_config(page_title="📸 Friends Photo Dashboard", layout="wide")

st.title("📸 Friends Photo Dashboard")

st.markdown("""
Welcome to your **Group Photo Dashboard**! 🎉  

1. Upload your photos into the shared Google Drive folder.  
2. This dashboard automatically shows all uploaded photos.  
3. Click any photo to open/download it in full size.  
""")

photos = list_images(FOLDER_ID)

if not photos:
    st.warning("⚠️ No photos found. Make sure your folder is shared with the Service Account.")
else:
    cols = st.columns(4)  # 4 photos per row
    for idx, photo in enumerate(photos):
        with cols[idx % 4]:
            st.image(photo["thumbnailLink"], caption=photo["name"])
            st.markdown(f"[🔗 View / Download]({photo['webViewLink']})")

