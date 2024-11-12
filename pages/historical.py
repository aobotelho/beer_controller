import pandas as pd
import streamlit as st
from glob import glob
import altair as alt
from datetime import date

BREW_SESSION_FOLDER = './data/brew_sessions'
IMAGES_FOLDER = './data/images'
PUMP_ON = False
PUMP_OFF = True


def load_brew_sessions_names() -> list:
    return [x.replace(f"{BREW_SESSION_FOLDER}/", "") for x in glob(f"{BREW_SESSION_FOLDER}/*")]

if __name__ == '__main__':
    col_1,col_2,col_3 = st.columns([2,5,2])
    
    col_1.image(f'{IMAGES_FOLDER}/logo_white.png')
    col_3.image(f'{IMAGES_FOLDER}/logo_white.png')
    
    with col_2: 
        st.markdown(f'## Beer controller')
        st.markdown(f'##### {date.today()}')
        st.markdown(f'##### Historical brew sessions')
    
    st.session_state['selected_brew_session'] = st.selectbox('Which brew session you want to load?', load_brew_sessions_names(), index = None)

    if st.session_state['selected_brew_session']:
        df_log = pd.read_csv(
            f"{BREW_SESSION_FOLDER}/{st.session_state['selected_brew_session']}/log.csv",
            sep = ",")
        df_log.timestamp = pd.to_datetime(df_log.timestamp)

        col_1, col_2 = st.columns([7,3])
        with col_1:
            st.slider("Points to plot filter", min_value = 0, max_value = df_log.shape[0], value = (0, df_log.shape[0]), key = "time_filter")
        
        with col_2:
            options = ["Pump", "Recirc."]
            st.pills("Show ON/OFF", options, selection_mode="multi", key = 'show_on_off')
        
        df_log = df_log.loc[st.session_state['time_filter'][0]:st.session_state['time_filter'][1]]
        
        ax = df_log.plot.line(x = 'timestamp',y= 'temperature', rot= 45)
        
        if 'Pump' in st.session_state['show_on_off']:
            df_pump_on_off_change = df_log.loc[df_log['pump_on_off'].diff().fillna(True)]
            on_values = df_pump_on_off_change.loc[df_pump_on_off_change['pump_on_off'],'timestamp'].values
            off_values = df_pump_on_off_change.loc[~df_pump_on_off_change['pump_on_off'],'timestamp'].values
            
            first = True
            for item in on_values:
                if first:
                    ax.axvline(x = item, linestyle=':', color = 'g', label = 'Pump ON')
                    first = False
                else:
                    ax.axvline(x = item, linestyle=':', color = 'g')

            first = True
            for item in off_values:
                if first:
                    ax.axvline(x = item, linestyle=':', color = 'r', label = 'Pump OFF')
                    first = False
                else:
                    ax.axvline(x = item, linestyle=':', color = 'r')

        if 'Recirc.' in st.session_state['show_on_off']:
            df_recirculate_on_off_change = df_log.loc[df_log['recirculate_on_off'].diff().fillna(True)]
            on_recirculate_values  = df_recirculate_on_off_change.loc[ df_recirculate_on_off_change['recirculate_on_off'],'timestamp'].values
            off_recirculate_values = df_recirculate_on_off_change.loc[~df_recirculate_on_off_change['recirculate_on_off'],'timestamp'].values

            first = True
            for item in on_recirculate_values:
                if first:
                    ax.axvline(x = item, linestyle='--', color = 'g', label = 'Recirculate ON')
                    first = False
                else:
                    ax.axvline(x = item, linestyle='--', color = 'g')

            first = True
            for item in off_recirculate_values:
                if first:
                    ax.axvline(x = item, linestyle='--', color = 'r', label = 'Recirculate OFF')
                    first = False
                else:
                    ax.axvline(x = item, linestyle='--', color = 'r')
        ax.legend()

        st.pyplot(ax.figure)

        st.pyplot(df_log.plot.line(x = 'timestamp',y= 'resistance_power', rot= 45).figure)
