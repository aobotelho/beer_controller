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
    
    
    pwm = HardwarePWM(pwm_channel=PWN_CHANNEL, hz=50, chip=2)
    pwm.start(0)


    col_1, col_2, col_3 = st.columns([3,3,4])
    with col_3:
        st.write("\n\n\n   ")
        st.slider("Resistor power", 0, 100, key = "RESISTOR_POWER",format="%d%%")
        
    
    pwm.start(st.session_state['RESISTOR_POWER'])
