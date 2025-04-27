'''
📈 Flowchart Diagram: Video Landscape ➡️ Portrait Converter

flowchart TD
    A[Start] --> B[User uploads video]
    B --> C[Analyze video width and height]
    C --> D{Is width < height?}
    D -- Yes --> E[Resize to target height directly]
    D -- No --> F[Crop center horizontally to match 9:16]
    F --> G[Resize cropped video to target resolution]
    E --> H[Save video file]
    G --> H
    H --> I[Display processed video in Streamlit]
    I --> J[Allow user to download final portrait video]
    J --> K[End]
'''

import streamlit as st
import moviepy.editor as mp
import tempfile
import os

def convert_landscape_to_portrait(video_path, output_path, target_resolution=(1080, 1920)):
    clip = mp.VideoFileClip(video_path)
    
    clip_width, clip_height = clip.size
    target_width, target_height = target_resolution

    if clip_width < clip_height:
        # Already portrait, just resize
        clip_resized = clip.resize(height=target_height)
    else:
        # Crop horizontally for portrait aspect ratio
        new_width = int(clip_height * target_width / target_height)
        x_center = clip_width / 2
        x1 = int(x_center - new_width / 2)
        x2 = int(x_center + new_width / 2)
        clip_cropped = clip.crop(x1=x1, y1=0, x2=x2, y2=clip_height)
        clip_resized = clip_cropped.resize(newsize=target_resolution)
    
    clip_resized.write_videofile(output_path, codec='libx264', audio_codec='aac')

# --- Streamlit App Interface ---
st.set_page_config(page_title="🎬 Video Landscape ➡️ Portrait Converter", layout="centered")

st.title("🎥 Video Landscape ➡️ Portrait Converter (Pixel Perfect)")

uploaded_file = st.file_uploader("Upload your landscape video", type=["mp4", "mov", "avi", "mkv"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_input:
        temp_input.write(uploaded_file.read())
        input_path = temp_input.name

    output_path = os.path.join(tempfile.gettempdir(), "output_portrait.mp4")

    with st.spinner("🔄 Processing your video..."):
        convert_landscape_to_portrait(input_path, output_path)

    st.success("✅ Conversion Completed!")

    st.subheader("🎬 Preview of Portrait Video:")
    st.video(output_path)

    with open(output_path, "rb") as file:
        st.download_button(
            label="📥 Download Portrait Video",
            data=file,
            file_name="portrait_video.mp4",
            mime="video/mp4"
        )
