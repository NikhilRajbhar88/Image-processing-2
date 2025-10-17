import streamlit as st
from rembg import remove
from PIL import Image
import numpy as np
import io
import cv2

st.set_page_config(page_title="Background Changer", page_icon="🎨", layout="wide")

st.title("🎨 Image Background Changer")
st.write("Upload an image and change its background to any color or custom image!")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    input_image = Image.open(uploaded_file).convert("RGBA")
    st.image(input_image, caption="Original Image", use_container_width=True)

    with st.spinner("Removing background..."):
        # Remove background using rembg
        output_image = remove(input_image)
        st.success("Background removed successfully!")

    st.image(output_image, caption="Background Removed", use_container_width=True)

    # Options to choose background type
    st.subheader("🎨 Choose Background Option")
    bg_option = st.radio("Select Background Type", ["Solid Color", "Custom Image"])

    final_image = None

    if bg_option == "Solid Color":
        # Choose background color
        color = st.color_picker("Pick a background color", "#00b4d8")

        # Create solid background
        bg = Image.new("RGBA", output_image.size, color)
        final_image = Image.alpha_composite(bg, output_image)
        st.image(final_image, caption="New Background", use_container_width=True)

    elif bg_option == "Custom Image":
        bg_file = st.file_uploader("Upload a background image", type=["jpg", "jpeg", "png"])
        if bg_file:
            bg_image = Image.open(bg_file).convert("RGBA")
            bg_image = bg_image.resize(output_image.size)

            final_image = Image.alpha_composite(bg_image, output_image)
            st.image(final_image, caption="New Background", use_container_width=True)

    # Download option
    if final_image is not None:
        buf = io.BytesIO()
        final_image.save(buf, format="PNG")
        byte_im = buf.getvalue()

        st.download_button(
            label="Download Final Image",
            data=byte_im,
            file_name="background_changed.png",
            mime="image/png"
        )
