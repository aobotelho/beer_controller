from random import randrange
import pandas as pd
import streamlit as st
from datetime import datetime
from common_functions import import_constants

class Temp_Beer_controller:
    def __init__(self):
        self.constants = import_constants()
        pass

    def get_temp(self,dummy_read = True):
        return randrange(30,41,1) if dummy_read else None

    def read_temp_file(self):
        try:
            df_log = pd.read_csv(
                f'{self.constants["BREW_SESSION_FOLDER"]}/{st.session_state["new_brew_session_id"]}/log.csv',
                sep = ","
            )
            df_log.timestamp = pd.to_datetime(df_log.timestamp)
            df_log['temperature'] = df_log['temperature'].astype('float64')
        except:
            df_log = pd.DataFrame(columns = self.constants["DATAFRAME_COLUMNS"])
        
        return df_log

    def write_temp_file(self,temp_dataframe):
        temp_dataframe.to_csv(f'{self.constants["BREW_SESSION_FOLDER"]}/{st.session_state["new_brew_session_id"]}/log.csv',sep = ',', index = False)

    def update_temp(self, dummy_read = True):
        df_temp = self.read_temp_file()

        new_temp = self.get_temp(dummy_read = dummy_read)

        if st.session_state["MANUAL_RESISTOR_POWER_TOGGLE"]:
            resistor_power = st.session_state["MANUAL_RESISTOR_POWER"] / 100
        else:
            resistor_power = st.session_state["AUTOMATIC_RESISTOR_POWER"]

        df_new_temp = pd.DataFrame(
            [[
                datetime.now(),
                new_temp,
                self.constants["PUMP_ON"][st.session_state["PUMP_ON_OFF"]]["PIN_MODE"],
                self.constants["RECIRCULATE_ON"][st.session_state["RECIRCULATE_ON_OFF"]]["PIN_MODE"],
                resistor_power,
                st.session_state["ramps_params"][st.session_state["CURRENT_RAMP_COUNTER"]]["name"],
                float(st.session_state["ramps_params"][st.session_state["CURRENT_RAMP_COUNTER"]]["temp"]),
                st.session_state["ramps_params"][st.session_state["CURRENT_RAMP_COUNTER"]]["time"] 
            ]],
            columns = self.constants["DATAFRAME_COLUMNS"]
        )

        if not df_temp.empty:
            df_temp = pd.concat(
                [
                    df_temp,
                    df_new_temp
                ], ignore_index= True)
        else:
            df_temp = df_new_temp.copy()
        
        self.write_temp_file(temp_dataframe = df_temp)

        return new_temp, df_temp
        
        
