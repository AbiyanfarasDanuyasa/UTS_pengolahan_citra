import streamlit as st
import cv2
import numpy as np
from matplotlib import pyplot as plt

# Mengatur tema Streamlit
def set_theme():
    # Mengubah tampilan latar belakang menjadi gradien
    st.markdown(
        """
        <style>
        .reportview-container {
            background: linear-gradient(to bottom, #2e2e2e, #101010) !important;
            color: #EAEAEA !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    # Mengubah tampilan tombol menjadi 'rounded' dan menambahkan efek hover
    st.markdown(
        """
        <style>
        .title-wrapper {
            perspective: 1000px;
            perspective-origin: center;
            overflow: hidden;
        }
        .title-wrapper h1 {
            position: relative;
            transition: all 0.3s;
            transform-origin: center;
            transform-style: preserve-3d;
            backface-visibility: hidden;
        }
        .title-wrapper:hover h1 {
            transform: rotateX(360deg);
        }
        .css-2trqyj:focus:not(:active) {
            box-shadow: none !important;
        }
        .css-2trqyj:not(:active) {
            box-shadow: none !important;
        }
        .css-2trqyj {
            border-radius: 12px !important;
            background-color: #1f77b4 !important;
            color: white !important;
        }
        .css-2trqyj:hover {
            background-color: #105399 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Fungsi untuk mengubah gambar ke mode HSV
def convert_to_hsv(image):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    return hsv_image

# Fungsi untuk menghitung dan menampilkan histogram gambar
def compute_histogram(image):
    colors = ('b', 'g', 'r')
    fig, ax = plt.subplots(figsize=(6, 4))
    for i, col in enumerate(colors):
        histogram = cv2.calcHist([image], [i], None, [256], [0, 256])
        ax.plot(histogram, color=col)
        ax.set_xlim([0, 256])
    ax.set_title('Histogram')
    ax.set_xlabel('Pixel Value')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)

# Fungsi untuk menyesuaikan brightness dan contrast gambar
def adjust_brightness_contrast(image, brightness, contrast):
    adjusted = cv2.convertScaleAbs(image, alpha=contrast/127.0, beta=brightness)
    return adjusted

# Fungsi untuk mencari kontur pada gambar
def find_contours(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def main():
    # Mengatur tema Streamlit
    set_theme()

    # Judul aplikasi dengan gaya teks yang berbeda
    st.markdown(
        """
        <div class="title-wrapper">
            <h1 style="font-size: 48px; text-align: center; color: #F08080;
                text-shadow: 2px 2px 4px #000000;">Aplikasi Proses Gambar</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Upload gambar
    uploaded_file = st.file_uploader("Upload Image", type=['jpg', 'jpeg', 'png'])

    if uploaded_file is not None:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, 1)

        # Menampilkan gambar asli
        st.subheader('Original Image')
        st.image(image, channels="BGR", use_column_width=True)

        # Sidebar untuk menyesuaikan brightness dan contrast
        brightness = st.sidebar.slider('Brightness', -100, 100, 0)
        contrast = st.sidebar.slider('Contrast', -100, 100, 0)

        # Menambahkan tombol untuk setiap fungsi
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button('Convert to HSV'):
                hsv_image = convert_to_hsv(image)
                st.subheader('HSV Image')
                st.image(hsv_image, channels="HSV", use_column_width=True)

        with col2:
            if st.button('Compute Histogram'):
                st.subheader('Histogram')
                compute_histogram(image)

        with col3:
            if st.button('Adjust Brightness and Contrast'):
                adjusted_image = adjust_brightness_contrast(image, brightness, contrast)
                st.subheader('Adjusted Image')
                st.image(adjusted_image, channels="BGR", use_column_width=True)

        with col4:
            if st.button('Find Contours'):
                contours = find_contours(image)
                st.subheader('Contours')
                image_with_contours = cv2.drawContours(image.copy(), contours, -1, (0, 255, 0), 2)
                st.image(image_with_contours, channels="BGR", use_column_width=True)

        # Menampilkan teks dengan gaya berbeda
        st.markdown(
            """
            <h3 style="color: #F08080; text-shadow: 1px 1px 2px #000000;">Manipulasi Gambar Selesai!</h3>
            """,
            unsafe_allow_html=True
        )

if _name_ == '_main_':
    main()
