import pandas as pd
import streamlit as st
from glob import glob
import altair as alt
from datetime import date

RUN_FOLDER = './data/runs'
IMAGES_FOLDER = './data/images'
PUMP_ON = False
PUMP_OFF = True


def load_runs_names() -> list:
    return [x.replace(f"{RUN_FOLDER}/", "") for x in glob(f"{RUN_FOLDER}/*")]

if __name__ == '__main__':
    col_1,col_2,col_3 = st.columns([2,5,2])
    
    col_1.image(f'{IMAGES_FOLDER}/logo_white.png')
    col_3.image(f'{IMAGES_FOLDER}/logo_white.png')
    
    with col_2: 
        st.markdown(f'## Beer controller')
        st.markdown(f'##### {date.today()}')
        st.markdown(f'##### Historical brew sessions')
    
    st.session_state['selected_brew_session'] = st.selectbox('Which brew session you want to load?', load_runs_names(), index = None)

    if st.session_state['selected_brew_session']:
        df_log = pd.read_csv(
            f"{RUN_FOLDER}/{st.session_state['selected_brew_session']}/log.csv",
            sep = ",")
        df_log.timestamp = pd.to_datetime(df_log.timestamp)
        
        df_pump_on_off_change = df_log[df_log['pump_on_off'] != df_log['pump_on_off'].shift(-1)]

        on_values = df_pump_on_off_change.loc[df_pump_on_off_change['pump_on_off'],'timestamp'].values
        off_values = df_pump_on_off_change.loc[~df_pump_on_off_change['pump_on_off'],'timestamp'].values


        ax = df_log.plot.line(x = 'timestamp',y= 'temperature', rot= 45)
        
        first = True
        for item in on_values:
            if first:
                ax.axvline(x = item, linestyle='--', color = 'g', label = 'Pump ON')
                first = False
            else:
                ax.axvline(x = item, linestyle='--', color = 'g')

        first = True
        for item in off_values:
            if first:
                ax.axvline(x = item, linestyle='--', color = 'r', label = 'Pump OFF')
                first = False
            else:
                ax.axvline(x = item, linestyle='--', color = 'r')
        ax.legend()

        st.pyplot(ax.figure)

        st.pyplot(df_log.plot.line(x = 'timestamp',y= 'resistance_power', rot= 45).figure)
