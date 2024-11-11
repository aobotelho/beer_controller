import pandas as pd
import streamlit as st
from glob import glob
import os
from datetime import date
import json
from time import sleep


RUN_FOLDER = './data/runs'
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

CREATE_DUMMY_RUN = True



def load_runs_names() -> list:
    return [x.replace(f"{RUN_FOLDER}/", "") for x in glob(f"{RUN_FOLDER}/*")]


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
        st.markdown(f'##### {date.today()}')
        st.markdown(f'##### Historical brew sessions')
    ########################################################################################################################
    #
    # /Constant, dont change
    #
    ########################################################################################################################
    

    st.text_input('What is the new run name (ID)?', key = 'new_run_id')

    # if 'START_RUN' not in st.session_state:
    
    #     if 'CONFIG_STARTED' not in st.session_state:
    #         st.session_state['CONFIG_STARTED'] = False
        

    #     if st.session_state['new_run_id']:
    #         if st.session_state['new_run_id'] in load_runs_names() and not st.session_state['CONFIG_STARTED']:
    #             st.warning(f"Name ** {st.session_state['new_run_id']} ** already exists. Please choose a new one")
    #             del st.session_state['new_run_id']
    #         else:
    #             st.markdown(f"Ok, I will create {st.session_state['new_run_id']} run")
            
    #             if not st.session_state['CONFIG_STARTED']:
    #                 os.makedirs(f"{RUN_FOLDER}/{st.session_state['new_run_id']}")
    #                 st.session_state['CONFIG_STARTED'] = True

    #             col_1,col_2 = st.columns([3,6])
            
    #             with col_1:
    #                 st.selectbox("How many ramps?", options= range(1,11),index = 0, key = "ramps")
                
    #             with col_2:
    #                 for ramp_num in range(st.session_state['ramps']):
    #                     col_1_temp, col_2_temp, col_3_temp = st.columns([1,1,3])
    #                     with col_1_temp:
    #                         st.text_input(f"Ramp {ramp_num + 1 } temp:", key = f"ramp_temp_{ramp_num}")
    #                     with col_2_temp:
    #                         st.text_input(f"Ramp {ramp_num + 1 } time:", key = f"ramp_time_{ramp_num}")
    #                     with col_3_temp:
    #                         st.text_input(f"Ramp {ramp_num + 1 } name:", key = f"ramp_name_{ramp_num}")
                        
                            
    #             st.session_state['ramps_params'] = [{
    #                 "name": st.session_state[f'ramp_name_{num}'], 
    #                 "temp": st.session_state[f'ramp_temp_{num}'],
    #                 "time": st.session_state[f'ramp_time_{num}']
    #             } for num in range(st.session_state['ramps'])]

    #             def start_run():
    #                 with open(f"{RUN_FOLDER}/{st.session_state['new_run_id']}/config.json","w") as fout: 
    #                     json.dump({
    #                         "id":st.session_state['new_run_id'],
    #                         "ramps_params": st.session_state['ramps_params']
    #                     }, fout)
    #                 st.session_state['CONFIG_STARTED']  = False
    #                 st.session_state['START_RUN']       = True
                    
                
    #             st.button("Start run?", on_click=start_run)

    # else:
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
    if True: #st.session_state['START'] or 'RUN_STARTED' in st.session_state:
        st.session_state['RUN_STARTED'] = True
        
        if CREATE_DUMMY_RUN:
            if 'dummy_run_counter' not in st.session_state or st.session_state['dummy_run_counter'] == 24:
                st.session_state['dummy_run_counter'] = -1

            st.session_state['dummy_run_counter'] += 1 
            
            df_log_dummy =  pd.read_csv(f"{RUN_FOLDER}/dummy/log.csv",sep = ",")
            
            try:
                df_log = pd.read_csv(
                f"{RUN_FOLDER}/{st.session_state['new_run_id']}/log.csv",
                sep = ",")
                df_log.timestamp = pd.to_datetime(df_log.timestamp)
            except:
                st.write(st.session_state['new_run_id'])
                df_log = pd.DataFrame(columns = df_log_dummy.columns)
            
            df_log = pd.concat(
                [
                    df_log,
                    df_log_dummy.loc[st.session_state['dummy_run_counter']:st.session_state['dummy_run_counter']]
                ], ignore_index= True)

            df_log.timestamp = pd.to_datetime(df_log.timestamp)
            df_log.to_csv(f"{RUN_FOLDER}/{st.session_state['new_run_id']}/log.csv",sep = ",", index = False)
            
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
            
            
            
            
            
            
            
            
            sleep(1)
            st.rerun()