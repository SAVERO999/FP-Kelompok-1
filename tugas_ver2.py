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
            title="Plot Data ECG (a) ",
            xaxis_title="Elapsed Time (s)",
            yaxis_title="Amplitude",
        )
        st.plotly_chart(fig_zoomed)
        new_title = '<p style="font-family:Georgia; color: black; font-size: 20px;">Nilai FS</p>'
        st.markdown(new_title, unsafe_allow_html=True)
        fs = 125
        st.write(fs)
        new_title = '<p style="font-family:Georgia; color: black; font-size: 20px;">Jumlah Semua Data</p>'
        st.markdown(new_title, unsafe_allow_html=True)
        jumlahdata = int(np.size(y))
        st.write(jumlahdata)
        
        return elapsed_time, y
    else:
        st.write('Please upload an ECG data file to get started.')
        return None, None

def dirac(x): 
    if x == 0:
        dirac_delta = 1
    else:
        dirac_delta = 0
    
    return dirac_delta

h = []
g = []
n_list = []

for n in range(-2, 2):
    n_list.append(n)
    temp_h = 1/8 * (dirac(n-1) + 3*dirac(n) + 3*dirac(n+1) + dirac(n+2))
    h.append(temp_h)
    temp_g = -2 * (dirac(n) - dirac(n+1))
    g.append(temp_g)

# Hw = []
# Gw = []

Hw = np.zeros(20000)
Gw = np.zeros(20000)
fs=125
i_list = []
for i in range (0,fs+1):
    i_list.append(i)
    reG = 0
    imG = 0
    reH = 0
    imH = 0
    for k in range(-2,2):
      reG = reG + g[k+abs(-2)]*np.cos(k*2*np.pi*i/fs)
      imG = imG - g[k+abs(-2)]*np.sin(k*2*np.pi*i/fs)
      reH = reH + h[k+abs(-2)]*np.cos(k*2*np.pi*i/fs)
      imH = imH - h[k+abs(-2)]*np.sin(k*2*np.pi*i/fs)
    temp_Hw = np.sqrt((reH**2)+(imH**2))
    temp_Gw = np.sqrt((reG**2)+(imG**2))
    Hw[i] = temp_Hw
    Gw[i] = temp_Gw
i_list = i_list[0:round(fs/2)+1]

Q = np.zeros((9, round(fs/2) + 1))

for i in range(round(fs/2) + 1):
    i_list.append(i)
    Q[1][i] = Gw[i]
    Q[2][i] = Gw[2*i] * Hw[i]
    Q[3][i] = Gw[4*i] * Hw[2*i] * Hw[i]
    Q[4][i] = Gw[8*i] * Hw[4*i] * Hw[2*i] * Hw[i]
    Q[5][i] = Gw[16*i] * Hw[8*i] * Hw[4*i] * Hw[2*i] * Hw[i]
    Q[6][i] = Gw[32*i] * Hw[16*i] * Hw[8*i] * Hw[4*i] * Hw[2*i] * Hw[i]
    Q[7][i] = Gw[64*i] * Hw[32*i] * Hw[16*i] * Hw[8*i] * Hw[4*i] * Hw[2*i] * Hw[i]
    Q[8][i] = Gw[128*i] * Hw[64*i] * Hw[32*i] * Hw[16*i] * Hw[8*i] * Hw[4*i] * Hw[2*i] * Hw[i]

T1 = round(2**(1-1))-1
T2 = round(2**(2-1))-1
T3 = round(2**(3-1))-1
T4 = round(2**(4-1))-1
T5 = round(2**(5-1))-1
Delay1 = T5-T1
Delay2 = T5-T2
Delay3 = T5-T3
Delay4 = T5-T4
Delay5 = T5-T5

def process_ecg(min_n, max_n, ecg, g, h):
    w2fm = np.zeros((5, max_n - min_n + 1))
    s2fm = np.zeros((5, max_n - min_n + 1))

    for n in range(min_n, max_n + 1):
        for j in range(1, 6):
            w2fm[j-1, n - min_n] = 0
            s2fm[j-1, n - min_n] = 0
            for k in range(-1, 3):
                index = round(n - 2**(j-1) * k)
                if 0 <= index < len(ecg):
                    w2fm[j-1, n - min_n] += g[k+1] * ecg[index]
                    s2fm[j-1, n - min_n] += h[k+1] * ecg[index]

    return w2fm, s2fm

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
    st.markdown("<h1 style='text-align: center; color: red;'>🫀ENCYCLOPEDIA</h1>", unsafe_allow_html=True)
    new_title = '<p style="font-family:Georgia; color:blue; font-size: 23px; text-align: left;">1. Apa yang dimaksud HRV?</p>'
    st.markdown(new_title, unsafe_allow_html=True)
    new_title = '<p style="font-family:Georgia; color:black; font-size: 20px; text-align: justify;">HRV secara sederhana adalah ukuran variasi waktu antara setiap detak jantung. Variasi ini dikendalikan oleh bagian primitif dari sistem saraf yang disebut sistem saraf otonom (ANS). Sistem ini bekerja di belakang layar, secara otomatis mengatur detak jantung, tekanan darah, pernapasan, dan pencernaan di antara tugas-tugas utama lainnya. ANS dibagi lagi menjadi dua komponen besar: sistem saraf simpatis dan parasimpatis, yang juga dikenal sebagai mekanisme fight-or-flight dan respons relaksasi.</p>'
    st.markdown(new_title, unsafe_allow_html=True)
    new_title = '<p style="font-family:Georgia; color:blue; font-size: 23px; text-align: left;">2. Bagaimana cara kerja HRV?</p>'
    st.markdown(new_title, unsafe_allow_html=True)
    new_title = '<p style="font-family:Georgia; color:black; font-size: 20px; text-align: justify;">Jantung Anda berdetak dengan kecepatan tertentu setiap saat. Denyut tersebut berubah tergantung pada apa yang sedang Anda lakukan saat itu. Denyut jantung yang lebih lambat terjadi ketika Anda sedang beristirahat atau santai, dan denyut yang lebih cepat terjadi ketika Anda sedang aktif, stres, atau ketika Anda dalam bahaya. Terdapat variabilitas dalam detak jantung Anda berdasarkan kebutuhan tubuh dan pola pernapasan Anda. Obat-obatan tertentu dan perangkat medis - seperti alat pacu jantung - juga dapat memengaruhi variabilitas detak jantung Anda. Variabilitas detak jantung Anda juga cenderung menurun secara normal seiring bertambahnya usia.</p>'
    st.markdown(new_title, unsafe_allow_html=True)
    content = """
    <iframe id='Video 1' width='560' height='315' src='https://www.youtube.com/embed/MUhtAXPvVnE' frameborder='0' allow='accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture' allowfullscreen></iframe>
    """
    st.markdown(content, unsafe_allow_html=True)
    st.link_button("Go to video", "https://youtu.be/MUhtAXPvVnE?si=rvYo04B8FCIcPT3I")

if selected == "Input Data":
    elapsed_time, y = upload_and_process_file()

if selected == "DWT":
    sub_selected1 = st.sidebar.radio(
        "",
        ["Filter Coef", "Mallat", "Filter Bank "],
        index=0
    )
    if sub_selected1 == 'Filter Coef':
            optimizer_options4 = [' ', 'h(n)', 'g(n)', 'Hw', 'Gw','Qj(f)']
            selected_optimizer4 = st.selectbox('Penurunan inverse fourier transform', optimizer_options4)
            if selected_optimizer4 == 'h(n)':
                fig = go.Figure(data=[go.Bar(x=n_list, y=h)])
                fig.update_layout(title='h(n) Plot', xaxis_title='n', yaxis_title='g(n)',template='plotly_dark')
                st.plotly_chart(fig)
            if selected_optimizer4 == 'g(n)':
                fig = go.Figure(data=[go.Bar(x=n_list, y=g)])
                fig.update_layout(title='g(n) Plot', xaxis_title='n', yaxis_title='g(n)',template='plotly_dark')
                st.plotly_chart(fig)
            if selected_optimizer4 == 'Hw':
                fig = go.Figure(data=go.Scatter(x=i_list, y=Hw[:len(i_list)]))
                fig.update_layout(title='Hw Plot', xaxis_title='i', yaxis_title='Gw',template='plotly_dark')
                st.plotly_chart(fig)
            if selected_optimizer4 == 'Gw':
                fig = go.Figure(data=go.Scatter(x=i_list, y=Gw[:len(i_list)]))
                fig.update_layout(title='Gw Plot', xaxis_title='i', yaxis_title='Gw',template='plotly_dark')
                st.plotly_chart(fig)
            if selected_optimizer4 == 'Qj(f)':
                traces = []
                for i in range(1, 9):
                 trace = go.Scatter(x=i_list, y=Q[i], mode='lines', name=f'Q[{i}]')
                 traces.append(trace)
                
                
                 layout = go.Layout(title='Qj (f)',
                                   xaxis=dict(title=''),
                                   yaxis=dict(title=''),
                                   template='plotly_dark'
                )
                
                
                 fig = go.Figure(data=traces, layout=layout)
                
                
                 st.plotly_chart(fig)
    if sub_selected1 == 'Mallat':
            optimizer_options5 = ['', 'Delay', 'w2fm','s2fm','gabungan']
            selected_optimizer5 = st.selectbox('', optimizer_options5)
            if selected_optimizer5 == 'Delay':
                data = {
                    "": ["T1", "T2", "T3","T4","T5"],
                    "Hasil": [T1, T2, T3,T4,T5]
                }
                df = pd.DataFrame(data)
                
                # Buat tabel menggunakan Plotly
                fig = go.Figure(data=[go.Table(
                    columnwidth=[80, 20],  # Set column width
                    header=dict(values=list(df.columns),
                                fill_color='red',  # Ubah warna header menjadi merah
                                align='left',
                                line_color='darkslategray',
                                height=30),  # Set header height
                    cells=dict(values=[df[""], df["Hasil"]],
                               fill_color='white',  # Ubah warna sel menjadi merah
                               align='left',
                               line_color='darkslategray',
                               height=25,  # Set cell height
                               font_size=12,  # Set font size
                               ),
                )])
                
                # Set layout to adjust the table size
                fig.update_layout(
                    width=800,
                    height=200,
                    margin=dict(l=10, r=10, t=10, b=10)
                )
                
                # Tampilkan tabel
                st.plotly_chart(fig)
                
                data = {
                    "": ["Delay1","Delay2","Delay3","Delay4","Delay5"],
                    "Hasil": [Delay1,Delay2,Delay3,Delay4,Delay5]
                }
                df = pd.DataFrame(data)
                
                # Buat tabel menggunakan Plotly
                fig = go.Figure(data=[go.Table(
                    columnwidth=[80, 20],  # Set column width
                    header=dict(values=list(df.columns),
                                fill_color='red',  # Ubah warna header menjadi merah
                                align='left',
                                line_color='darkslategray',
                                height=30),  # Set header height
                    cells=dict(values=[df[""], df["Hasil"]],
                               fill_color='white',  # Ubah warna sel menjadi merah
                               align='left',
                               line_color='darkslategray',
                               height=25,  # Set cell height
                               font_size=12,  # Set font size
                               ),
                )])
                
                # Set layout to adjust the table size
                fig.update_layout(
                    width=800,
                    height=200,
                    margin=dict(l=10, r=10, t=10, b=10)
                )
                
                # Tampilkan tabel
                st.plotly_chart(fig)
            
            if selected_optimizer5 == 'w2fm':
                # Function to create and display a plot for a given series
                def create_plot(n_values, series, index, series_name):
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=n_values, y=series, mode='lines', name=f'{series_name}[{index+1},n]'))
                    fig.update_layout(
                        title=f'{series_name}({index+1})f'
                    )
                    st.plotly_chart(fig)
                
                # Create and show separate plots for each w2fm series
                for i in range(5):
                    create_plot(n_values, w2fm_values[i], i, 'w2fm')
                    
            if selected_optimizer5 == 's2fm':
                # Function to create and display a plot for a given series
                def create_plot(n_values, series, index, series_name):
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=n_values, y=series, mode='lines', name=f'{series_name}[{index+1},n]'))
                    fig.update_layout(
                        title=f'{series_name}({index+1})f'
                    )
                    st.plotly_chart(fig)
                
                # Create and show separate plots for each w2fm series
                for i in range(5):
                    create_plot(n_values, s2fm_values[i], i, 's2fm')
            if selected_optimizer5 == 'gabungan':
                n_values = np.arange(min_n, max_n + 1)
                for i in range(0, 5):
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=n_values, y=w2fm[i], mode='lines', name=f'w2fm {i+1}'))
                    fig.add_trace(go.Scatter(x=n_values, y=s2fm[i], mode='lines', name=f's2fm {i+1}'))
                    fig.update_layout(
                        title=f'w2fm and s2fm ({i+1})f',
                        template='plotly_dark'
                    )
                    st.plotly_chart(fig)

