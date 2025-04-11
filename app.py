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
