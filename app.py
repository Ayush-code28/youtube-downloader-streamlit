import streamlit as st
import subprocess
import os
import uuid
import shutil

st.set_page_config(page_title="YouTube Downloader", layout="centered")

st.title("🎬 YouTube Downloader")
st.markdown("Download audio or video from YouTube with ease.")

url = st.text_input("📥 Enter YouTube URL")
download_type = st.selectbox("📁 Type", ["Video", "Audio"])
quality = st.selectbox("🎧 Quality", ["best", "worst"])
custom_filename = st.text_input("📄 Custom filename (optional)")
is_playlist = st.checkbox("Download Playlist")
download_button = st.button("🚀 Download")

def download_youtube(url, download_type, quality, custom_filename, is_playlist):
    st.write("🔄 Processing download...")

    if not url:
        st.error("❌ Please enter a YouTube URL.")
        return

    # Create temp folder
    temp_dir = "temp_downloads"
    os.makedirs(temp_dir, exist_ok=True)

    unique_id = str(uuid.uuid4())[:8]
    output_template = os.path.join(temp_dir, f"{custom_filename}_{unique_id}_%(title)s.%(ext)s") if custom_filename else os.path.join(temp_dir, f"%(title)s.%(ext)s")

    playlist_flag = "--yes-playlist" if is_playlist else "--no-playlist"

    try:
        if download_type == "Audio":
            cmd = [
                "yt-dlp",
                playlist_flag,
                "-f", "bestaudio",
                "-x",
                "--audio-format", "mp3",
                "--ffmpeg-location", "/usr/bin/ffmpeg",
                "-o", output_template,
                url
            ]
        else:
            cmd = [
                "yt-dlp",
                playlist_flag,
                "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
                "--merge-output-format", "mp4",
                "--ffmpeg-location", "/usr/bin/ffmpeg",
                "-o", output_template,
                url
            ]

        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode != 0:
            st.error("❌ yt-dlp error:")
            st.code(result.stderr)
            return

        # Show download success and allow download
        downloaded_files = os.listdir(temp_dir)
        if not downloaded_files:
            st.warning("⚠️ Download completed, but file not found.")
        else:
            for file in downloaded_files:
                file_path = os.path.join(temp_dir, file)
                st.success(f"✅ File downloaded: {file}")
                with open(file_path, "rb") as f:
                    st.download_button(label=f"⬇️ Download {file}", data=f, file_name=file)

    except Exception as e:
        st.error(f"❌ Unexpected error: {e}")

    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)

if download_button:
    download_youtube(url, download_type, quality, custom_filename, is_playlist)
