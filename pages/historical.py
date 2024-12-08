import pandas as pd
import streamlit as st
from glob import glob
import json
from datetime import date
from common_functions import print_header, load_brew_sessions_names, plot_temperature


constants = json.load(open('./constants.json'))
constants["PUMP_ON"][False] = constants["PUMP_ON"]["False"]
constants["PUMP_ON"][True] = constants["PUMP_ON"]["True"]
constants["RECIRCULATE_ON"][False] = constants["RECIRCULATE_ON"]["False"]
constants["RECIRCULATE_ON"][True] = constants["RECIRCULATE_ON"]["True"]


if __name__ == '__main__':
    col_1,col_2,col_3 = st.columns([2,5,2])
    
    col_1.image(f'{constants["IMAGES_FOLDER"]}/logo_white.png')
    col_3.image(f'{constants["IMAGES_FOLDER"]}/logo_white.png')
    
    with col_2: 
        st.markdown(f'## Beer controller')
        st.markdown(f'##### {date.today()}')
        st.markdown(f'##### Historical brew sessions')
    
    st.session_state['selected_brew_session'] = st.selectbox('Which brew session you want to load?', load_brew_sessions_names(), index = None)

    if st.session_state['selected_brew_session']:
        df_log = pd.read_csv(
            f'{constants["BREW_SESSION_FOLDER"]}/{st.session_state["selected_brew_session"]}/log.csv',
            sep = ',')
        df_log.timestamp = pd.to_datetime(df_log.timestamp)

        col_1, col_2 = st.columns([7,3])
        with col_1:
            st.slider('Points to plot filter', min_value = 0, max_value = df_log.shape[0], value = (0, df_log.shape[0]), key = "time_filter")
        
        with col_2:
            options = ['Pump', 'Recirc.']
            st.pills('Show ON/OFF', options, selection_mode='multi', key = 'show_on_off')
        
        df_log = df_log.loc[st.session_state["time_filter"][0]:st.session_state["time_filter"][1]]

        plot_temperature(df_log,show_pump_on_off = 'Pump' in st.session_state["show_on_off"], show_recirc_on_off = 'Recirc.' in st.session_state["show_on_off"])

        st.pyplot(df_log.plot.line(x = 'timestamp',y= 'resistance_power', rot= 45).figure)
