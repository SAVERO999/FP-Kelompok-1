import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from streamlit_option_menu import option_menu
import math
import streamlit as st 



df = pd.read_csv('dataecginofix1.txt', sep='\s+', header=None)
ecg_signal = df[df.columns[0]]

# Calculate the number of samples
N = len(ecg_signal)

# Calculate the elapsed time
sample_interval = np.arange(0, N)
elapsed_time = sample_interval * (1/125)

# Center the ECG signal by subtracting the mean
y = ecg_signal/1e8

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






with st.sidebar:
    selected = option_menu("TUGAS 1", ["Home", "Signal Processing","DWT"], default_index=0)

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
  
if selected == "Signal Processing":
    # Plot using Plotly
    fig = go.Figure()
    
    # Add the ECG signal trace
    fig.add_trace(go.Scatter(x=elapsed_time, y=y, mode='lines', name='ECG Signal'))
    
    # Update the layout
    fig.update_layout(
        title='ECG Signal',
        xaxis_title='Elapsed Time (s)',
        yaxis_title='Amplitude',
        width=1000,
        height=400
    )
    
    # Show the plot
    st.plotly_chart(fig)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=elapsed_time[0:1000], y=y[0:1000], mode='lines', name='ECG (a)', line=dict(color='blue')))
    fig.update_layout(
        height=500,
        width=1500,
        title="ECG Signal",
        xaxis_title="Elapsed Time (s)",
        yaxis_title="Nilai",
    
    )
    st.plotly_chart(fig)

if selected == "DWT":
   sub_selected = st.sidebar.radio(
        "Pilih Metode HRV Analysis",
        ["Filter Coeffs", "Mallat", "Filter Bank"],
        index=0
    )

    
   if sub_selected  == 'Filter Coeffs':
     optimizer_options = ['', 'h(n) & g(n)', 'hw & gw','Qj (f)','q1(k)','q2(k)','q3(k)','q4(k)','q5(k)']
     selected_optimizer = st.selectbox('Segmentation', optimizer_options)
     if selected_optimizer == 'h(n) & g(n)':
        fig = go.Figure(data=[go.Bar(x=n_list, y=h)])
        fig.update_layout(title='h(n) Plot', xaxis_title='n', yaxis_title='g(n)')
        st.plotly_chart(fig)
         
        fig = go.Figure(data=[go.Bar(x=n_list, y=g)])
        fig.update_layout(title='g(n) Plot', xaxis_title='n', yaxis_title='g(n)')
        st.plotly_chart(fig)
     if selected_optimizer == 'hw & gw':
        fig = go.Figure(data=go.Scatter(x=i_list, y=Hw[:len(i_list)]))
        fig.update_layout(title='Hw Plot', xaxis_title='i', yaxis_title='Gw')
        st.plotly_chart(fig)
       
        fig = go.Figure(data=go.Scatter(x=i_list, y=Gw[:len(i_list)]))
        fig.update_layout(title='Gw Plot', xaxis_title='i', yaxis_title='Gw')
        st.plotly_chart(fig)
     
     if selected_optimizer == 'Qj (f)':
         for i in range(1, 9):
            trace = go.Scatter(x=i_list, y=Q[i], mode='lines', name=f'Q[{i}]')
            traces.append(trace)
            
            
            layout = go.Layout(title='Qj (f)',
                               xaxis=dict(title=''),
                               yaxis=dict(title=''))
            
            
            fig = go.Figure(data=traces, layout=layout)
            st.plotly_chart(fig)
     if selected_optimizer == 'q1(k)':
         fig = go.Figure(data=[go.Bar(x=k_list, y=qj[1][0:len(k_list)])])
         fig.update_layout(title='', xaxis_title='', yaxis_title='')
         st.plotly_chart(fig)
     if selected_optimizer == 'q2(k)':
         fig = go.Figure(data=[go.Bar(x=k_list, y=qj[2][0:len(k_list)])])
         fig.update_layout(title='', xaxis_title='', yaxis_title='')
         st.plotly_chart(fig)
     if selected_optimizer == 'q3(k)':
         fig = go.Figure(data=[go.Bar(x=k_list, y=qj[3][0:len(k_list)])])
         fig.update_layout(title='', xaxis_title='', yaxis_title='')
         st.plotly_chart(fig)
     if selected_optimizer == 'q4(k)':
         fig = go.Figure(data=[go.Bar(x=k_list, y=qj[4][0:len(k_list)])])
         fig.update_layout(title='', xaxis_title='', yaxis_title='')
         st.plotly_chart(fig)
         



        


    
   if sub_selected  == 'Mallat':
            st.title("t")
   if sub_selected  == 'Filter Bank':
            st.title("t")
        

    

    

    

    

  
         
        
         



