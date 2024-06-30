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





with st.sidebar:
    selected = option_menu("TUGAS 1", ["Home", "Signal Processing","HRV Analysis"], default_index=0)

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
        title="Plot Data ECG (a)",
        xaxis_title="Elapsed Time",
        yaxis_title="Nilai",
    
    )
    fig.show()


