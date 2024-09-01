import streamlit as st
from PIL import Image
import io
import os
from style_transfer import apply_style_transfer
from deepdream_generator import generate_deepdream
from image_captioning import generate_caption

st.set_page_config(page_title="VisionVerse", layout="wide")

def save_uploadedfile(uploadedfile):
    with open(uploadedfile.name, "wb") as f:
        f.write(uploadedfile.getbuffer())
    return uploadedfile.name

st.title("VisionVerse")

st.sidebar.title("Choose Your Option")
option = st.sidebar.radio("Select Processing Type", ["Style Transfer", "DeepDream", "Image Captioning"])

if option == "Style Transfer":
    st.header("Neural Style Transfer")
    
    col1, col2 = st.columns(2)
    
    with col1:
        content_file = st.file_uploader("Choose a content image", type=["png", "jpg", "jpeg"])
    
    with col2:
        style_file = st.file_uploader("Choose a style image", type=["png", "jpg", "jpeg"])

    if content_file and style_file:
        content_image = Image.open(content_file)
        style_image = Image.open(style_file)

        st.image(content_image, caption="Content Image", use_column_width=True)
        st.image(style_image, caption="Style Image", use_column_width=True)

        if st.button('Apply Style Transfer'):
            with st.spinner('Applying style transfer...'):
                content_path = save_uploadedfile(content_file)
                style_path = save_uploadedfile(style_file)

                result_image = apply_style_transfer(content_path, style_path)
            
            st.image(result_image, caption="Stylized Image", use_column_width=True)

            os.remove(content_path)
            os.remove(style_path)

elif option == "DeepDream":
    st.header("DeepDream Generator")
    
    uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        if st.button("Generate DeepDream"):
            with st.spinner('Generating DeepDream...'):
                result = generate_deepdream(image)
            st.image(result, caption="DeepDream Result", use_column_width=True)

elif option == "Image Captioning":
    st.header("Image Captioning")
    
    uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        if st.button("Generate Caption"):
            with st.spinner('Generating caption...'):
                image_path = save_uploadedfile(uploaded_file)
                caption = generate_caption(image_path)
                os.remove(image_path)
            st.write(f"Caption: {caption}")

st.sidebar.markdown("---")
st.sidebar.write("Created with ❤️ using Streamlit")