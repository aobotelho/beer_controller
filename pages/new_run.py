import pandas as pd
import streamlit as st
from glob import glob
import os
from datetime import datetime
import json
from time import sleep
import numpy as np


BREW_SESSION_FOLDER = './data/brew_sessions'
IMAGES_FOLDER = './data/images'
PUMP_ON = {
    False:{
        "IMAGE_NAME": "off_button.png",
        "PIN_MODE": False
    },
    True:{
        "IMAGE_NAME": "on_button.png",
        "PIN_MODE": True
    }
}
RECIRCULATE_ON = {
    False:{
        "IMAGE_NAME": "off_button.png",
        "PIN_MODE": False
    },
    True:{
        "IMAGE_NAME": "on_button.png",
        "PIN_MODE": True
    }
}

CREATE_DUMMY_BREW_SESSION = True

DATAFRAME_COLUMNS = ['timestamp','temperature','pump_on_off','recirculate_on_off','resistance_power']

def load_brew_sessions_names() -> list:
    return [x.replace(f"{BREW_SESSION_FOLDER}/", "") for x in glob(f"{BREW_SESSION_FOLDER}/*")]


if __name__ == '__main__':
    ########################################################################################################################
    #
    # Constant, dont change
    #
    ########################################################################################################################
    col_1,col_2,col_3 = st.columns([2,5,2])
    
    col_1.image(f'{IMAGES_FOLDER}/logo_white.png')
    col_3.image(f'{IMAGES_FOLDER}/logo_white.png')
    
    with col_2: 
        st.markdown(f'## Beer controller')
        st.markdown(f'##### {datetime.now()}')
        st.markdown(f'##### New brew sessions')
    ########################################################################################################################
    #
    # /Constant, dont change
    #
    ########################################################################################################################
    

    st.text_input('What is the new brew session name (ID)?', key = 'new_brew_session_id')

    if 'START_BREW_SESSION' not in st.session_state:
    
        if 'CONFIG_STARTED' not in st.session_state:
            st.session_state['CONFIG_STARTED'] = False
        

        if st.session_state['new_brew_session_id']:
            if st.session_state['new_brew_session_id'] in load_brew_sessions_names() and not st.session_state['CONFIG_STARTED']:
                st.warning(f"Name ** {st.session_state['new_brew_session_id']} ** already exists. Please choose a new one")
                del st.session_state['new_brew_session_id']
            else:
                st.markdown(f"Ok, I will create {st.session_state['new_brew_session_id']} brew session")
            
                if not st.session_state['CONFIG_STARTED']:
                    os.makedirs(f"{BREW_SESSION_FOLDER}/{st.session_state['new_brew_session_id']}")
                    st.session_state['CONFIG_STARTED'] = True

                col_1,col_2 = st.columns([3,6])
            
                with col_1:
                    st.selectbox("How many ramps?", options= range(1,11),index = 0, key = "ramps")
                
                with col_2:
                    for ramp_num in range(st.session_state['ramps']):
                        col_1_temp, col_2_temp, col_3_temp = st.columns([1,1,3])
                        with col_1_temp:
                            st.text_input(f"Ramp {ramp_num + 1 } temp:", key = f"ramp_temp_{ramp_num}")
                        with col_2_temp:
                            st.text_input(f"Ramp {ramp_num + 1 } time:", key = f"ramp_time_{ramp_num}")
                        with col_3_temp:
                            st.text_input(f"Ramp {ramp_num + 1 } name:", key = f"ramp_name_{ramp_num}")
                        
                            
                st.session_state['ramps_params'] = [{
                    "name": st.session_state[f'ramp_name_{num}'], 
                    "temp": st.session_state[f'ramp_temp_{num}'],
                    "time": st.session_state[f'ramp_time_{num}']
                } for num in range(st.session_state['ramps'])]

                def start_brew_session():
                    with open(f"{BREW_SESSION_FOLDER}/{st.session_state['new_brew_session_id']}/config.json","w") as fout: 
                        json.dump({
                            "id":st.session_state['new_brew_session_id'],
                            "ramps_params": st.session_state['ramps_params']
                        }, fout)
                    st.session_state['CONFIG_STARTED']      = False
                    st.session_state['START_BREW_SESSION']  = True
                    
                
                st.button("Start brew session?", on_click=start_brew_session)

    else:
        col_1, col_2, col_3 = st.columns([3,3,4])

        with col_1:
            if 'PUMP_ON_OFF' not in st.session_state:
                st.session_state['PUMP_ON_OFF'] = PUMP_ON[False]['PIN_MODE']
            
            def toggle_pump():
                st.session_state['PUMP_ON_OFF'] = not st.session_state['PUMP_ON_OFF']
            
            
            _, col_2_button, _ = st.columns([1,5,1])
            with col_2_button:
                st.markdown("### Pump.")
            
                st.image(f"{IMAGES_FOLDER}/{ PUMP_ON[st.session_state['PUMP_ON_OFF']]['IMAGE_NAME'] }")

                st.button("ON / OFF", on_click=toggle_pump, key = "PUMP", use_container_width = True)
        
        with col_2:
            if 'RECIRCULATE_ON_OFF' not in st.session_state:
                st.session_state['RECIRCULATE_ON_OFF'] = RECIRCULATE_ON[False]['PIN_MODE']
            
            def toggle_recirculate():
                st.session_state['RECIRCULATE_ON_OFF'] = not st.session_state['RECIRCULATE_ON_OFF']
            
            _, col_2_button, _ = st.columns([1,5,1])
            with col_2_button:
                st.markdown("### Recirc.")
            
                st.image(f"{IMAGES_FOLDER}/{ RECIRCULATE_ON[st.session_state['RECIRCULATE_ON_OFF']]['IMAGE_NAME'] }")

                st.button("ON / OFF", on_click=toggle_recirculate, key = "RECIRCULATE", use_container_width = True)

        with col_3:
            st.write("\n\n\n   ")
            st.slider("Resistor power", 0, 100, key = "RESISTOR_POWER",format="%d%%")
        
        st.button("START", key = "START", use_container_width = True)
        if st.session_state['START'] or 'BREW_SESSION_STARTED' in st.session_state:
            st.session_state['BREW_SESSION_STARTED'] = True

            if CREATE_DUMMY_BREW_SESSION:
                from random import randrange
                
                try:
                    df_log = pd.read_csv(
                        f"{BREW_SESSION_FOLDER}/{st.session_state['new_brew_session_id']}/log.csv",
                        sep = ","
                    )
                    df_log.timestamp = pd.to_datetime(df_log.timestamp)
                except:
                    df_log = pd.DataFrame(columns = DATAFRAME_COLUMNS)
                
                df_log = pd.concat(
                    [
                        df_log,
                        pd.DataFrame(
                            [[
                                datetime.now(),
                                randrange(1,100,1),
                                PUMP_ON[st.session_state['PUMP_ON_OFF']]['PIN_MODE'],
                                RECIRCULATE_ON[st.session_state['RECIRCULATE_ON_OFF']]['PIN_MODE'],
                                st.session_state['RESISTOR_POWER']
                            ]],
                            columns = DATAFRAME_COLUMNS
                        )
                    ], ignore_index= True)

                
                df_log.to_csv(f"{BREW_SESSION_FOLDER}/{st.session_state['new_brew_session_id']}/log.csv",sep = ",", index = False)
                
                df_log = df_log.tail(20)
                
                df_pump_on_off_change = df_log.loc[df_log['pump_on_off'].diff().fillna(True)]
                on_values = df_pump_on_off_change.loc[df_pump_on_off_change['pump_on_off'],'timestamp'].values
                off_values = df_pump_on_off_change.loc[~df_pump_on_off_change['pump_on_off'],'timestamp'].values


                df_recirculate_on_off_change = df_log.loc[df_log['recirculate_on_off'].diff().fillna(True)]
                on_recirculate_values  = df_recirculate_on_off_change.loc[ df_recirculate_on_off_change['recirculate_on_off'],'timestamp'].values
                off_recirculate_values = df_recirculate_on_off_change.loc[~df_recirculate_on_off_change['recirculate_on_off'],'timestamp'].values


                ax = df_log.plot.line(x = 'timestamp',y= 'temperature', rot= 45)
                
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

                st.pyplot(df_log.plot.line(x = 'timestamp',y= 'resistance_power', rot= 45).figure)
                
                
                
                
                
                
                
                
                sleep(1)
                st.rerun()