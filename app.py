import streamlit as st
import numpy as np
import cv2
from PIL import Image
import io

def encode_message(img, message):
    message += "####"  # Delimiter to mark end of message
    binary_msg = ''.join([format(ord(char), '08b') for char in message])
    data_index = 0
    img_data = img.flatten().astype(np.uint8)  # ensure correct type

    for i in range(len(binary_msg)):
        if data_index < len(img_data):
            # use safer masking to stay within 0–255
            pixel = int(img_data[data_index])
            pixel = (pixel & 0b11111110) | int(binary_msg[i])
            img_data[data_index] = pixel
            data_index += 1
        else:
            st.error("Message too large for this image!")
            break

    encoded_img = img_data.reshape(img.shape)
    return encoded_img



def decode_message(img):
    binary_data = ""
    img_data = img.flatten()

    for pixel in img_data:
        binary_data += str(pixel & 1)

    # Convert binary data to string
    all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    decoded_msg = ""
    for byte in all_bytes:
        decoded_msg += chr(int(byte, 2))
        if decoded_msg.endswith("####"):
            break
    return decoded_msg[:-4]


# --- Streamlit UI ---

st.set_page_config(page_title="Image Secrets", page_icon="🕵️‍♂️", layout="wide")
st.title("🕵️‍♂️ Image Secrets")
st.write("Hide secret messages inside images securely and reveal them anytime!")

menu = st.sidebar.radio("Select Mode", ["Encrypt Message", "Decrypt Message"])

if menu == "Encrypt Message":
    st.header("🔒 Hide Message inside Image")
    uploaded_file = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        img = np.array(Image.open(uploaded_file))
        st.image(img, caption="Original Image", use_container_width=True)

        secret_message = st.text_area("Enter your secret message:")
        if st.button("Encrypt and Download"):
            if secret_message.strip() == "":
                st.warning("Please enter a message to hide!")
            else:
                encoded_img = encode_message(img.copy(), secret_message)
                result = Image.fromarray(encoded_img.astype(np.uint8))

                buf = io.BytesIO()
                result.save(buf, format="PNG")
                byte_im = buf.getvalue()

                st.success("✅ Message successfully hidden inside image!")
                st.download_button(
                    label="Download Encrypted Image",
                    data=byte_im,
                    file_name="encoded_image.png",
                    mime="image/png"
                )

elif menu == "Decrypt Message":
    st.header("🔍 Reveal Hidden Message from Image")
    uploaded_file = st.file_uploader("Upload the Encrypted Image", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        img = np.array(Image.open(uploaded_file))
        st.image(img, caption="Encrypted Image", use_container_width=True)

        if st.button("Reveal Message"):
            message = decode_message(img)
            st.success("✅ Message Revealed!")
            st.text_area("Hidden Message:", message, height=150)
