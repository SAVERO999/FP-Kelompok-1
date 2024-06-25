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


########
df = pd.read_csv('dataecginofix1.txt', sep='\s+', header=None)
ecg_signal = df[df.columns[0]]

# Calculate the number of samples
N = len(ecg_signal)

# Calculate the elapsed time
sample_interval = np.arange(0, N)
elapsed_time = sample_interval * (1/125)

# Center the ECG signal by subtracting the mean
y = ecg_signal/1e8

fs=125
jumlahdata = int(np.size(elapsed_time ))

def dirac(x):
    if x == 0:
        dirac_delta = 1
    else:
        dirac_delta = 0
    result = dirac_delta
    return result

h = []
g = []
n_list = []

for n in range(-2, 2):
    n_list.append(n)
    temp_h = 1/8 * (dirac(n-1) + 3*dirac(n) + 3*dirac(n+1) + dirac(n+2))
    h.append(temp_h)
    temp_g = -2 * (dirac(n) - dirac(n+1))
    g.append(temp_g)
import numpy as np
Hw = np.zeros(20000)
Gw = np.zeros(20000)
i_list = []
fs =125
for i in range(0,fs + 1):
    i_list.append(i)
    reG = 0
    imG = 0
    reH = 0
    imH = 0
    for k in range(-2, 2):
        reG = reG + g[k + abs(-2)] * np.cos(k * 2 * np.pi * i / fs)
        imG = imG - g[k + abs(-2)] * np.sin(k * 2 * np.pi * i / fs)
        reH = reH + h[k + abs(-2)] * np.cos(k * 2 * np.pi * i / fs)
        imH = imH - h[k + abs(-2)] * np.sin(k * 2 * np.pi * i / fs)
    temp_Hw = np.sqrt((reH**2) + (imH**2))
    temp_Gw = np.sqrt((reG**2) + (imG**2))
    Hw[i] = temp_Hw
    Gw[i] = temp_Gw

i_list = i_list[0:round(fs/2)+1]
Q = np.zeros((9, round(fs/2) + 1))

# Generate the i_list and fill Q with the desired values
i_list = []
for i in range(0, round(fs/2) + 1):
    i_list.append(i)
    Q[1][i] = Gw[i]
    Q[2][i] = Gw[2*i] * Hw[i]
    Q[3][i] = Gw[4*i] * Hw[2*i] * Hw[i]
    Q[4][i] = Gw[8*i] * Hw[4*i] * Hw[2*i] * Hw[i]
    Q[5][i] = Gw[16*i] * Hw[8*i] * Hw[4*i] * Hw[2*i] * Hw[i]
    Q[6][i] = Gw[32*i] * Hw[16*i] * Hw[8*i] * Hw[4*i] * Hw[2*i] * Hw[i]
    Q[7][i] = Gw[64*i] * Hw[32*i] * Hw[16*i] * Hw[8*i] * Hw[4*i] * Hw[2*i] * Hw[i]
    Q[8][i] = Gw[128*i] * Hw[64*i] * Hw[32*i] * Hw[16*i] * Hw[8*i] * Hw[4*i] * Hw[2*i] * Hw[i]

traces = []
qj = np.zeros ((6, 10000))
k_list = []
j= 1
a = -(round (2**j) + round (2**(j-1)) - 2 )
b=-(1- round(2**(j-1)))+1
for k in range (a,b):
  k_list.append(k)
  qj[1][k+abs(a)] = -2 * ( dirac(k) - dirac(k+1) )
k_list = []

j= 2
a = -(round (2**j) + round (2**(j-1)) - 2 )
b=-(1- round(2**(j-1)))+1

for k in range (a,b):
  k_list.append(k)
  qj[2][k+abs(a)] = -1/4* ( dirac(k-1) + 3*dirac(k)  + 2*dirac(k+1)  - 2*dirac(k+2) - 3*dirac(k+3) - dirac(k+4))

k_list = []
j=3
a=-(round(2**j) + round(2**(j-1))-2)
b = - (1 - round(2**(j-1))) + 1
for k in range (a,b):
  k_list.append(k)
  qj[3][k+abs(a)] = -1/32*(dirac(k-3) + 3*dirac(k-2) + 6*dirac(k-1) + 10*dirac(k)
  + 11*dirac(k+1) + 9*dirac(k+2) + 4*dirac(k+3) - 4*dirac(k+4) - 9*dirac(k+5)
  - 11*dirac(k+6) - 10*dirac(k+7) - 6*dirac(k+8) - 3*dirac(k+9) - dirac(k+10))

k_list = []
j=4
a=-(round(2**j) + round(2**(j-1))-2)
b = - (1 - round(2**(j-1))) + 1
for k in range (a,b):
  k_list.append(k)
  qj [4][k+abs(a)] = -1/256*(dirac(k-7) + 3*dirac(k-6) + 6*dirac(k-5) + 10*dirac(k-4) + 15*dirac (k-3)
  + 21*dirac(k-2) + 28*dirac(k-1) + 36*dirac(k) + 41*dirac(k+1) + 43*dirac(k+2)
  + 42*dirac(k+3) + 38*dirac(k+4) + 31*dirac(k+5) + 21*dirac(k+6) + 8*dirac(k+7)
  - 8*dirac(k+8) - 21*dirac(k+9) - 31*dirac(k+10) - 38*dirac(k+11) - 42*dirac(k+12)
  - 43*dirac(k+13) - 41*dirac(k+14) - 36*dirac(k+15) - 28*dirac(k+16) - 21*dirac(k+17)
  - 15*dirac(k+18) - 10*dirac(k+19) - 6*dirac(k+20) - 3*dirac(k+21) - dirac(k+22))

k_list = []
j=5
a=-(round(2**j) + round(2**(j-1))-2)
b = - (1 - round(2**(j-1))) + 1
for k in range (a,b):
  k_list.append(k)
  qj[5][k+abs(a)] = -1/(512)*(dirac(k-15) + 3*dirac(k-14) + 6*dirac(k-13) + 10*dirac(k-12) + 15*dirac(k-11) + 21*dirac(k-10)
+ 28*dirac(k-9) + 36*dirac(k-8) + 45*dirac(k-7) + 55*dirac(k-6) + 66*dirac(k-5) + 78*dirac(k-4)
+ 91*dirac(k-3) + 105*dirac(k-2) + 120*dirac(k-1) + 136*dirac(k) + 149*dirac(k+1) + 159*dirac(k+2)
+ 166*dirac(k+3) + 170*dirac(k+4) + 171*dirac(k+5) + 169*dirac(k+6) + 164*dirac(k+7) + 156*dirac(k+8)
+ 145*dirac(k+9) + 131*dirac(k+10) + 114*dirac(k+11) + 94*dirac(k+12) + 71*dirac(k+13) + 45 *dirac(k+14)
+ 16*dirac(k+15) - 16*dirac(k+16) - 45*dirac(k+17) - 71*dirac(k+18) - 94*dirac(k+19) - 114*dirac (k+20)
- 131*dirac(k+21) - 145*dirac(k+22) - 156*dirac(k+23) - 164*dirac(k+24) - 169*dirac(k+25)
- 171*dirac(k+26) - 170*dirac(k+27) - 166*dirac(k+28) - 159*dirac(k+29) - 149*dirac(k+30)
- 136*dirac(k+31) - 120*dirac(k+32) - 105*dirac(k+33) - 91*dirac(k+34) - 78*dirac(k+35)
- 66*dirac(k+36) - 55*dirac(k+37) - 45*dirac(k+38) - 36*dirac(k+39) - 28*dirac(k+40)
- 21*dirac(k+41) - 15*dirac(k+42) - 10*dirac(k+43) - 6*dirac(k+44) - 3*dirac(k+45)
- dirac(k+46))
    
T1= round (2**(1-1))-1
T2 = round(2** (2-1)) - 1
T3 = round(2** (3-1)) - 1
T4 = round(2**(4-1)) - 1
T5 = round(2**(5-1))- 1
Delay1= T5-T1
Delay2= T5-T2
Delay3= T5-T3
Delay4= T5-T4
Delay5= T5-T5
ecg=y

min_n = 0 * fs
max_n = 8 * fs 


def process_ecg(min_n, max_n, ecg, g, h):
    w2fm = np.zeros((5, max_n - min_n + 1))
    s2fm = np.zeros((5, max_n - min_n + 1))

    for n in range(min_n, max_n + 1):
        for j in range(1, 6):
            w2fm[j-1, n - min_n] = 0
            s2fm[j-1, n - min_n] = 0
            for k in range(-1, 3):
                index = round(n - 2**(j-1) * k)
                if 0 <= index < len(ecg):  # Ensure the index is within bounds
                    w2fm[j-1, n - min_n] += g[k+1] * ecg[index]  # g[k+1] to match Pascal's array index starting from -1
                    s2fm[j-1, n - min_n] += h[k+1] * ecg[index]  # h[k+1] to match Pascal's array index starting from -1

    return w2fm, s2fm

# Compute w2fm and s2fm
w2fm, s2fm = process_ecg(min_n, max_n, ecg, g, h)

# Prepare data for plotting
n_values = np.arange(min_n, max_n + 1)
w2fm_values = [w2fm[i, :] for i in range(5)]  # Equivalent to w2fm[1,n] to w2fm[5,n] in original code (0-based index)
s2fm_values = [s2fm[i, :] for i in range(5)]  # Equivalent to s2fm[1,n] to s2fm[5,n] in original code (0-based index)

w2fb = np.zeros((6, len(ecg) + T5))


n_list = list(range(len(ecg)))

# Perform calculations
for n in n_list:
    for j in range(1, 6):
        w2fb[1][n + T1] = 0
        w2fb[2][n + T2] = 0
        w2fb[3][n + T3] = 0
        a = -(round(2**j) + round(2**(j - 1)) - 2)
        b = -(1 - round(2**(j - 1)))
        for k in range(a, b + 1):
            index = n - (k + abs(a))
            if 0 <= index < len(ecg):
                w2fb[1][n + T1] += qj[1][k + abs(a)] * ecg[index]
                w2fb[2][n + T2] += qj[2][k + abs(a)] * ecg[index]
                w2fb[3][n + T3] += qj[3][k + abs(a)] * ecg[index]
                w2fb[4][n + T3] += qj[4][k + abs(a)] * ecg[index]
                w2fb[5][n + T3] += qj[5][k + abs(a)] * ecg[index]

# Create and display plots for each DWT level
figs = []
n = np.arange(1000)













with st.sidebar:
    selected = option_menu("FP", ["Home","Encyclopedia", "Data Input","DWT"], default_index=0)

if selected == "Home":
   st.title('Project ASN Kelompok 1')
   st.subheader("Anggota kelompok")
   new_title = '<p style="font-family:Georgia; color: black; font-size: 15px;">Farhan Majid Ibrahim - 5023211049</p>'
   st.markdown(new_title, unsafe_allow_html=True)
   new_title = '<p style="font-family:Georgia; color: black; font-size: 15px;">Nayla Pramudhita Putri Pertama - 5023211012</p>'
   st.markdown(new_title, unsafe_allow_html=True)
   new_title = '<p style="font-family:Georgia; color: black; font-size: 15px;">Mohammad Rayhan Amirul Haq Siregar - 5023211045</p>'
   st.markdown(new_title, unsafe_allow_html=True)
   new_title = '<p style="font-family:Georgia; color: black; font-size: 15px;">Reynard Prastya Savero - 5023211042</p>'
   st.markdown(new_title, unsafe_allow_html=True)
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
    new_title = '<p style="font-family:Georgia; color:black; font-size: 20px; text-align: Justify;">Jantung Anda berdetak dengan kecepatan tertentu setiap saat. Denyut tersebut berubah tergantung pada apa yang sedang Anda lakukan saat itu. Denyut jantung yang lebih lambat terjadi ketika Anda sedang beristirahat atau santai, dan denyut yang lebih cepat terjadi ketika Anda sedang aktif, stres, atau ketika Anda dalam bahaya. Terdapat variabilitas dalam detak jantung Anda berdasarkan kebutuhan tubuh dan pola pernapasan Anda. Obat-obatan tertentu dan perangkat medis - seperti alat pacu jantung - juga dapat memengaruhi variabilitas detak jantung Anda. Variabilitas detak jantung Anda juga cenderung menurun secara normal seiring bertambahnya usia.</p>'
    st.markdown(new_title, unsafe_allow_html=True)
    # HTML content with the new YouTube video embedded
    content = """

    <iframe id='Video 1' width='560' height='315' src='https://www.youtube.com/embed/MUhtAXPvVnE' frameborder='0' allow='accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture' allowfullscreen></iframe>
     """

    # Display the HTML content
    st.markdown(content, unsafe_allow_html=True)
    st.link_button("Go to video", "https://youtu.be/MUhtAXPvVnE?si=rvYo04B8FCIcPT3I")
    
if selected == "Data Input":
    st.title('Data & Graphic Input')
    st.header("Data Input")
    st.write(df)

    # Create the figure with Plotly
    fig = go.Figure(data=go.Scatter(x=elapsed_time, y=y, mode='lines'))
    fig.update_layout(
        title="Original Signal",
        xaxis_title="Elapsed Time",
        yaxis_title="Amplitude (mV)",
        xaxis=dict(showline=True, showgrid=True),
        yaxis=dict(showline=True, showgrid=True),
        
    )
    
    # Display the figure in Streamlit
    st.header("Graphic Input")
    st.plotly_chart(fig) 
    
    
    new_title = '<p style="font-family:Georgia; color: black; font-size: 20px;">Nilai FS</p>'
    st.markdown(new_title, unsafe_allow_html=True)
    st.write(fs)
    new_title = '<p style="font-family:Georgia; color: black; font-size: 20px;">Jumlah Semua Data</p>'
    st.markdown(new_title, unsafe_allow_html=True)
    st.write(jumlahdata)
    


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
        if sub_selected1 == 'Filter Bank':
            
                for i in range(1, 6):
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=n, y=w2fb[i][:len(n)], mode='lines', name=f'Orde {i}'))
                    fig.update_layout(
                        title=f'Plot Orde {i}',
                        xaxis_title='elapsed_time',
                        yaxis_title='Nilai',
                        template='plotly_dark',
                        height=400,
                        width=1500,
                    )
                    figs.append(fig)
                
                for fig in figs:
                    st.plotly_chart(fig)



        


    
    



        
    






 


        
        






        





        
        
    




    


         
