import pandas as pd
import streamlit as st
from glob import glob
from rpi_hardware_pwm import HardwarePWM
import gpiod
from datetime import datetime
pd.set_option('future.no_silent_downcasting', True)


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
    },
    "PIN_NUMBER": 4
}
RECIRCULATE_ON = {
    False:{
        "IMAGE_NAME": "off_button.png",
        "PIN_MODE": False
    },
    True:{
        "IMAGE_NAME": "on_button.png",
        "PIN_MODE": True
    },
    "PIN_NUMBER": 15
}

CREATE_DUMMY_BREW_SESSION = True

DATAFRAME_COLUMNS = ['timestamp','temperature','pump_on_off','recirculate_on_off','resistance_power','ramp_name', 'temperature_setpoint','ramp_time']

def load_brew_sessions_names() -> list:
    return [x.replace(f"{BREW_SESSION_FOLDER}/", "") for x in glob(f"{BREW_SESSION_FOLDER}/*")]

PWN_CHANNEL = 0


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
    
    
    if 'RESISTOR_POWER' not in st.session_state:
        pwm = HardwarePWM(pwm_channel=PWN_CHANNEL, hz=50, chip=2)
        pwm.start(0)

    if 'PUMP_ON_OFF' not in st.session_state:
        chip = gpiod.Chip('gpiochip4')
        pump_var = chip.get_line(PUMP_ON['PIN_NUMBER'])
        recirc_var = chip.get_line(RECIRCULATE_ON['PIN_NUMBER'])

        pump_var.request(consumer="PUMP", type=gpiod.LINE_REQ_DIR_OUT)
        recirc_var.request(consumer="RECIRC", type=gpiod.LINE_REQ_DIR_OUT)

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
        
    
    pump_var.set_value(st.session_state['PUMP_ON_OFF'])
    recirc_var.set_value(st.session_state['RECIRCULATE_ON_OFF'])
    pwm.start(st.session_state['RESISTOR_POWER'])