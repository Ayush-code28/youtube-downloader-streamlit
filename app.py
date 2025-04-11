# import streamlit as st
# import subprocess
# import os
# import uuid
# import shutil

# st.set_page_config(page_title="YouTube Downloader", layout="centered")

# st.title("🎬 YouTube Downloader")
# st.markdown("Download audio or video from YouTube with ease.")

# url = st.text_input("📥 Enter YouTube URL")
# download_type = st.selectbox("📁 Type", ["Video", "Audio"])
# quality = st.selectbox("🎧 Quality", ["best", "worst"])
# custom_filename = st.text_input("📄 Custom filename (optional)")
# is_playlist = st.checkbox("Download Playlist")
# download_button = st.button("🚀 Download")

# def download_youtube(url, download_type, quality, custom_filename, is_playlist):
#     st.write("🔄 Processing download...")

#     if not url:
#         st.error("❌ Please enter a YouTube URL.")
#         return

#     # Create temp folder
#     temp_dir = "temp_downloads"
#     os.makedirs(temp_dir, exist_ok=True)

#     unique_id = str(uuid.uuid4())[:8]
#     output_template = os.path.join(temp_dir, f"{custom_filename}_{unique_id}_%(title)s.%(ext)s") if custom_filename else os.path.join(temp_dir, f"%(title)s.%(ext)s")

#     playlist_flag = "--yes-playlist" if is_playlist else "--no-playlist"

#     try:
#         if download_type == "Audio":
#             cmd = [
#                 "yt-dlp",
#                 playlist_flag,
#                 "-f", "bestaudio",
#                 "-x",
#                 "--audio-format", "mp3",
#                 "--ffmpeg-location", "/usr/bin/ffmpeg",
#                 "-o", output_template,
#                 url
#             ]
#         else:
#             cmd = [
#                 "yt-dlp",
#                 playlist_flag,
#                 "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
#                 "--merge-output-format", "mp4",
#                 "--ffmpeg-location", "/usr/bin/ffmpeg",
#                 "-o", output_template,
#                 url
#             ]

#         result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

#         if result.returncode != 0:
#             st.error("❌ yt-dlp error:")
#             st.code(result.stderr)
#             return

#         # Show download success and allow download
#         downloaded_files = os.listdir(temp_dir)
#         if not downloaded_files:
#             st.warning("⚠️ Download completed, but file not found.")
#         else:
#             for file in downloaded_files:
#                 file_path = os.path.join(temp_dir, file)
#                 st.success(f"✅ File downloaded: {file}")
#                 with open(file_path, "rb") as f:
#                     st.download_button(label=f"⬇️ Download {file}", data=f, file_name=file)

#     except Exception as e:
#         st.error(f"❌ Unexpected error: {e}")

#     # Cleanup
#     shutil.rmtree(temp_dir, ignore_errors=True)

# if download_button:
#     download_youtube(url, download_type, quality, custom_filename, is_playlist)


import streamlit as st
import os
import subprocess
import shlex
import glob

st.set_page_config(page_title="YouTube Downloader", page_icon="🎬")

st.title("🎬 YouTube Downloader")
st.markdown("Download YouTube videos or audio as you like!")

# --- User Inputs ---
url = st.text_input("🔗 Enter YouTube Video or Playlist URL")
download_type = st.selectbox("📁 Select Download Type", ["Audio", "Video"])
quality = st.selectbox("🎧 Select Quality", ["best", "worst"])
custom_filename = st.text_input("✏️ Custom Filename (optional)")
is_playlist = st.checkbox("📂 Download as Playlist")

# --- Download Button ---
if st.button("🚀 Start Download"):
    if not url:
        st.warning("Please enter a YouTube URL.")
    else:
        st.info(f"Downloading {download_type} from:\n{url}")

        try:
            filename = custom_filename.strip().replace(" ", "_")
            output_template = f"{filename}_%(title)s.%(ext)s" if filename else "%(title)s.%(ext)s"
            playlist_flag = "--yes-playlist" if is_playlist else "--no-playlist"

            # Build command
            if download_type == "Audio":
                cmd = f'yt-dlp {playlist_flag} -f "bestaudio[ext=m4a]/bestaudio" -x --audio-format mp3 -o "{output_template}" "{url}"'
            else:
                cmd = f'yt-dlp {playlist_flag} -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]" --merge-output-format mp4 -o "{output_template}" "{url}"'

            st.text("Running command...")
            subprocess.run(shlex.split(cmd), check=True)

            # Search for files
            ext = "mp3" if download_type == "Audio" else "mp4"
            pattern = f"{filename}_*.{ext}" if filename else f"*.{ext}"
            files_found = glob.glob(pattern)

            if files_found:
                for file in files_found:
                    st.success(f"✅ Downloaded: {file}")
                    with open(file, "rb") as f:
                        st.download_button(label="⬇️ Download File", data=f, file_name=os.path.basename(file))
            else:
                st.warning("⚠️ Download finished but file not found.")

        except subprocess.CalledProcessError as e:
            st.error(f"yt-dlp error:\n{e}")
        except Exception as e:
            st.error(f"General error:\n{e}")
