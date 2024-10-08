import pandas as pd
import streamlit as st
from glob import glob
import altair as alt

RUN_FOLDER = './data/runs'

def load_runs() -> list:
    return [x.replace(f"{RUN_FOLDER}/", "") for x in glob(f"{RUN_FOLDER}/*")]

if __name__ == '__main__':
    col_1,col_2,col_3 = st.columns([0.2,1,0.5])
    with col_1: 
        st.image('./data/images/logo_white.png', use_column_width = True)
    
    with col_2: 
        st.markdown('# Beer controller')

    with col_3:
        st.markdown('''
            Created by: Andre Botelho
            
            Github: aobotelho
            ''')
    
    st.markdown('## Load run')
    selected_run = st.selectbox('Which run you want to load?', load_runs())

    if selected_run:
        df_temperature = pd.read_csv(
            f"{RUN_FOLDER}/{selected_run}/temperature.csv",
            sep = ",")
        
        temperature_chart = alt.Chart(df_temperature).mark_line().encode(
            x = alt.X("timestamp").title("Timestamp").axis(labelAngle = -45), 
            y = alt.Y("temperature").title("Temperature (°C)")
        )
        st.altair_chart(temperature_chart, use_container_width = True)