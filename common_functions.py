import json
from glob import glob
import streamlit as st
from datetime import datetime

constants = json.load(open('./constants.json'))

def load_brew_sessions_names() -> list:
    return [x.replace(f'{constants["BREW_SESSION_FOLDER"]}/', '') for x in glob(f'{constants["BREW_SESSION_FOLDER"]}/*')]

def print_header():
    col_1,col_2,col_3 = st.columns([2,5,2])
    
    col_1.image(f'{constants["IMAGES_FOLDER"]}/logo_white.png')
    col_3.image(f'{constants["IMAGES_FOLDER"]}/logo_white.png')
    
    with col_2: 
        st.markdown(f'## Beer controller')
        st.markdown(f'##### {datetime.now()}')
        st.markdown(f'##### New brew sessions')

    pass

def plot_temperature(df_to_plot, show_pump_on_off = False, show_recirc_on_off = False):
    
    if show_pump_on_off:
        df_pump_on_off_change = df_to_plot.loc[df_to_plot["pump_on_off"].diff().fillna(True)]       
        on_values =  df_pump_on_off_change.loc[df_pump_on_off_change["pump_on_off"], 'timestamp'].values
        off_values = df_pump_on_off_change.loc[~df_pump_on_off_change["pump_on_off"],'timestamp'].values
    else:
        on_values = []
        off_values = []


    if show_recirc_on_off:
        df_recirculate_on_off_change = df_to_plot.loc[df_to_plot["recirculate_on_off"].diff().fillna(True)]
        on_recirculate_values  = df_recirculate_on_off_change.loc[ df_recirculate_on_off_change["recirculate_on_off"],'timestamp'].values
        off_recirculate_values = df_recirculate_on_off_change.loc[~df_recirculate_on_off_change["recirculate_on_off"],'timestamp'].values
    else:
        on_recirculate_values = []
        off_recirculate_values = []
    

    ax  = df_to_plot.plot.line(x = 'timestamp',y= ['temperature','temperature_setpoint'], rot= 45)
    
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
    ax.legend()

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