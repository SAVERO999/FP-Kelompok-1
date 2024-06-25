import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from streamlit_option_menu import option_menu
import math
import streamlit as st 
from streamlit_lottie import st_lottie
from st_click_detector import click_detector
import plotly.express as px

# Function to load data
def load_data(file):
    df = pd.read_csv(file, sep='\s+', header=None)
    return df

# Function to process ECG signal
def process_ecg_signal(df):
    ecg_signal = df[df.columns[0]]

    # Calculate the number of samples
    N = len(ecg_signal)

    # Calculate the elapsed time
    sample_interval = np.arange(0, N)
    elapsed_time = sample_interval * (1/125)

    # Center the ECG signal by dividing by 1e8
    y = ecg_signal / 1e8

    return elapsed_time, y

# Function to handle file upload and processing
def upload_and_process_file():
    uploaded_file = st.file_uploader('Upload your ECG data file', type=['txt', 'csv'])
    
    if uploaded_file is not None:
        df = load_data(uploaded_file)
        elapsed_time, y = process_ecg_signal(df)
        
        # Plot using Plotly
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=elapsed_time, y=y, mode='lines', name='ECG', line=dict(color='blue')))
        fig.update_layout(
            height=500,
            width=1500,
            title="Plot Data ECG (a)",
            xaxis_title="Elapsed Time (s)",
            yaxis_title="Amplitude",
        )
        st.plotly_chart(fig)
        
        # Additional Plot for the first 1000 samples
        fig_zoomed = go.Figure()
        fig_zoomed.add_trace(go.Scatter(x=elapsed_time[:1000], y=y[:1000], mode='lines', name='ECG (a)', line=dict(color='blue')))
        fig_zoomed.update_layout(
            height=500,
            width=1500,
            title="Plot Data ECG (a) - First 1000 Samples",
            xaxis_title="Elapsed Time (s)",
            yaxis_title="Amplitude",
        )
        st.plotly_chart(fig_zoomed)
        
        st.write('## Data Preview')
        st.write(df.head())
    else:
        st.write('Please upload an ECG data file to get started.')

# Streamlit app
with st.sidebar:
    selected = option_menu("FP", ["Home", "Encyclopedia", "Input Data", "DWT"], default_index=0)

if selected == "Home":
    st.title('Project ASN Kelompok 1')
    st.subheader("Anggota kelompok")
    members = [
        "Farhan Majid Ibrahim - 5023211049",
        "Nayla Pramudhita Putri Pertama - 5023211012",
        "Mohammad Rayhan Amirul Haq Siregar - 5023211045",
        "Reynard Prastya Savero - 5023211042"
    ]
    for member in members:
        st.markdown(f'<p style="font-family:Georgia; color: black; font-size: 15px;">{member}</p>', unsafe_allow_html=True)
    st_lottie("https://lottie.host/50914bbf-8aa3-4ac1-8ab7-d7d7882d51d5/QVzC4aV82R.json", height=400, width=400)

if selected == "Encyclopedia":
    # Main title
    st.markdown("<h1 style='text-align: center; color: red;'>🫀ENCYCLOPEDIA</h1>", unsafe_allow_html=True)
    # Subtitle
    new_title = '<p style="font-family:Georgia; color:blue; font-size: 23px; text-align: left;">1. Apa yang dimaksud HRV?</p>'
    st.markdown(new_title, unsafe_allow_html=True)
    new_title = '<p style="font-family:Georgia; color:black; font-size: 20px; text-align: justify;">HRV secara sederhana adalah ukuran variasi waktu antara setiap detak jantung. Variasi ini dikendalikan oleh bagian primitif dari sistem saraf yang disebut sistem saraf otonom (ANS). Sistem ini bekerja di belakang layar, secara otomatis mengatur detak jantung, tekanan darah, pernapasan, dan pencernaan di antara tugas-tugas utama lainnya. ANS dibagi lagi menjadi dua komponen besar: sistem saraf simpatis dan parasimpatis, yang juga dikenal sebagai mekanisme fight-or-flight dan respons relaksasi.</p>'
    st.markdown(new_title, unsafe_allow_html=True)
    new_title = '<p style="font-family:Georgia; color:blue; font-size: 23px; text-align: left;">2. Bagaimana cara kerja HRV?</p>'
    st.markdown(new_title, unsafe_allow_html=True)
    new_title = '<p style="font-family:Georgia; color:black; font-size: 20px; text-align: justify;">Jantung Anda berdetak dengan kecepatan tertentu setiap saat. Denyut tersebut berubah tergantung pada apa yang sedang Anda lakukan saat itu. Denyut jantung yang lebih lambat terjadi ketika Anda sedang beristirahat atau santai, dan denyut yang lebih cepat terjadi ketika Anda sedang aktif, stres, atau ketika Anda dalam bahaya. Terdapat variabilitas dalam detak jantung Anda berdasarkan kebutuhan tubuh dan pola pernapasan Anda. Obat-obatan tertentu dan perangkat medis - seperti alat pacu jantung - juga dapat memengaruhi variabilitas detak jantung Anda. Variabilitas detak jantung Anda juga cenderung menurun secara normal seiring bertambahnya usia.</p>'
    st.markdown(new_title, unsafe_allow_html=True)
    # HTML content with the new YouTube video embedded
    content = """
    <iframe id='Video 1' width='560' height='315' src='https://www.youtube.com/embed/MUhtAXPvVnE' frameborder='0' allow='accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture' allowfullscreen></iframe>
    """

    # Display the HTML content
    st.markdown(content, unsafe_allow_html=True)
    st.link_button("Go to video", "https://youtu.be/MUhtAXPvVnE?si=rvYo04B8FCIcPT3I")

if selected == "Input Data":
    upload_and_process_file()

if selected == "DWT":
    st.write("DWT functionality to be implemented here.")
