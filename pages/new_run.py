import pandas as pd
import streamlit as st
import os
import json
from time import sleep

from datetime import datetime
from common_functions import print_header, load_brew_sessions_names, plot_temperature, import_constants
from modules.pwm import PWM_Beer_controller
from modules.temp import Temp_Beer_controller

constants = import_constants()

def start_brew_session_function():
    with open(f'{constants["BREW_SESSION_FOLDER"]}/{st.session_state["new_brew_session_id"]}/config.json',"w") as fout: 
        json.dump({
            "id":st.session_state["new_brew_session_id"],
            "ramps_params": st.session_state["ramps_params"]
        }, fout)
    st.session_state["CONFIG_STARTED"]      = False
    st.session_state["START_BREW_SESSION"]  = True
    st.session_state["CURRENT_RAMP_COUNTER"] = 0

    pass
    
def config_new_brew_session():
    if st.session_state["new_brew_session_id"]:
        if st.session_state["new_brew_session_id"] in load_brew_sessions_names() and not st.session_state["CONFIG_STARTED"]:
            st.warning(f'Name ** {st.session_state["new_brew_session_id"]} ** already exists. Please choose a new one')
            del st.session_state["new_brew_session_id"]
        else:
            st.markdown(f'Ok, I will create {st.session_state["new_brew_session_id"]} brew session')
        
            if not st.session_state["CONFIG_STARTED"]:
                os.makedirs(f'{constants["BREW_SESSION_FOLDER"]}/{st.session_state["new_brew_session_id"]}')
                st.session_state["CONFIG_STARTED"] = True

            col_1,col_2 = st.columns([3,6])
        
            with col_1:
                st.selectbox("How many ramps?", options= range(1,11),index = 0, key = "ramps")
            
            with col_2:
                for ramp_num in range(st.session_state["ramps"]):
                    col_1_temp, col_2_temp, col_3_temp = st.columns([1,1,3])
                    with col_1_temp:
                        st.text_input(f'Ramp {ramp_num + 1 } temp:', key = f'ramp_temp_{ramp_num}')
                    with col_2_temp:
                        st.text_input(f'Ramp {ramp_num + 1 } time:', key = f'ramp_time_{ramp_num}')
                    with col_3_temp:
                        st.text_input(f'Ramp {ramp_num + 1 } name:', key = f'ramp_name_{ramp_num}')
                    
                        
            st.session_state["ramps_params"] = [{
                "name": st.session_state[f'ramp_name_{num}'], 
                "temp": st.session_state[f'ramp_temp_{num}'],
                "time": st.session_state[f'ramp_time_{num}']
            } for num in range(st.session_state["ramps"])]

            st.button("Start brew session?", on_click=start_brew_session_function)

def brew_session_header():
    col_1, col_2, col_3 = st.columns([3,3,4])

    with col_1:
        if 'PUMP_ON_OFF' not in st.session_state:
            st.session_state["PUMP_ON_OFF"] = constants["PUMP_ON"]["False"]["PIN_MODE"]
        
        def toggle_pump():
            st.session_state["PUMP_ON_OFF"] = not st.session_state["PUMP_ON_OFF"]
        
        
        _, col_2_button, _ = st.columns([1,5,1])
        with col_2_button:
            st.markdown('### Pump.')
        
            st.image(f'{constants["IMAGES_FOLDER"]}/{ constants["PUMP_ON"][st.session_state["PUMP_ON_OFF"]]["IMAGE_NAME"] }')

            st.button('ON / OFF', on_click=toggle_pump, key = 'PUMP', use_container_width = True)
    
    with col_2:
        if 'RECIRCULATE_ON_OFF' not in st.session_state:
            st.session_state["RECIRCULATE_ON_OFF"] = constants["RECIRCULATE_ON"]["False"]["PIN_MODE"]
        
        def toggle_recirculate():
            st.session_state["RECIRCULATE_ON_OFF"] = not st.session_state["RECIRCULATE_ON_OFF"]
        
        _, col_2_button, _ = st.columns([1,5,1])
        with col_2_button:
            st.markdown('### Recirc.')
        
            st.image(f'{constants["IMAGES_FOLDER"]}/{ constants["RECIRCULATE_ON"][st.session_state["RECIRCULATE_ON_OFF"]]["IMAGE_NAME"] }')

            st.button('ON / OFF', on_click=toggle_recirculate, key = 'RECIRCULATE', use_container_width = True)

    with col_3:
        st.write('\n\n\n   ')
        st.toggle('Manual resistor power?', value = True, key = 'MANUAL_RESISTOR_POWER_TOGGLE')        
        if st.session_state["MANUAL_RESISTOR_POWER_TOGGLE"]:
            st.slider('Resistor power', 0, 100, key = 'MANUAL_RESISTOR_POWER',format='%d%%')
            st.session_state["PWM"].set_pwm_power(st.session_state["MANUAL_RESISTOR_POWER"])
        else:
            if 'AUTOMATIC_RESISTOR_POWER' in st.session_state:
                st.progress(st.session_state["AUTOMATIC_RESISTOR_POWER"], text = f'Resistor power: {st.session_state["AUTOMATIC_RESISTOR_POWER"] * 100:0.2f}%')
    
def start_brew_session():
    st.session_state["BREW_SESSION_STARTED"] = True

if __name__ == '__main__':
    print_header()
    
    st.text_input('What is the new brew session name (ID)?', key = 'new_brew_session_id')

    if 'START_BREW_SESSION' not in st.session_state:
    
        if 'CONFIG_STARTED' not in st.session_state:
            st.session_state["CONFIG_STARTED"] = False
        
        config_new_brew_session()        

    else:
        if 'MANUAL_RESISTOR_POWER' not in st.session_state and 'AUTOMATIC_RESISTOR_POWER' not in st.session_state:
            st.session_state["PWM"] = PWM_Beer_controller(pwm_channel_var= constants["PWN_CHANNEL"], dummy_run = constants["CREATE_DUMMY_BREW_SESSION"])
        
        if 'TEMP_VAR' not in st.session_state:
            st.session_state["TEMP_VAR"] = Temp_Beer_controller()

        if not 'BREW_SESSION_STARTED' in st.session_state:
            st.button('START', key = 'START', use_container_width = True, on_click=start_brew_session)

        if 'BREW_SESSION_STARTED' in st.session_state:
            brew_session_header()

            _, df_log = st.session_state["TEMP_VAR"].update_temp(dummy_read = constants["CREATE_DUMMY_BREW_SESSION"])
            
            time_in_ramp = (datetime.now() - df_log.loc[df_log["ramp_name"] == st.session_state["ramps_params"][st.session_state["CURRENT_RAMP_COUNTER"]]["name"],'timestamp'].min()).total_seconds()

            plot_progress_bar = True
            if time_in_ramp > float(st.session_state["ramps_params"][st.session_state["CURRENT_RAMP_COUNTER"]]["time"]):
                st.session_state["CURRENT_RAMP_COUNTER"] += 1
                plot_progress_bar = False
                if st.session_state["CURRENT_RAMP_COUNTER"] > len(st.session_state["ramps_params"]):
                    st.stop()
            if plot_progress_bar:
                st.progress(time_in_ramp / float(st.session_state["ramps_params"][st.session_state["CURRENT_RAMP_COUNTER"]]["time"]))

            df_log = df_log.tail(20)

            st.session_state["AUTOMATIC_RESISTOR_POWER"] = st.session_state["PWM"].define_pwm_power(target_temp = float(st.session_state["ramps_params"][st.session_state["CURRENT_RAMP_COUNTER"]]["temp"]), read_temp = df_log["temperature"].mean())          
            
            
            if df_log.shape[0] > 0:
                plot_temperature(df_log,True,True)

                st.pyplot(df_log.plot.line(x = 'timestamp',y= 'resistance_power', rot= 45).figure)
                
            sleep(1)
            st.rerun()