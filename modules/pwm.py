from rpi_hardware_pwm import HardwarePWM

class PWM_Beer_controller:
    def __init__(self, pwm_channel_var, frequency_var = 50, chip_var  = 2, dummy_run = False):
        self.dummy_run = dummy_run
        if not self.dummy_run:
            self.pwm = HardwarePWM(pwm_channel=pwm_channel_var, hz=frequency_var, chip=chip_var)
            self.pwm.start(0)

        pass

    def set_pwm_power(self,pwm_power):
        if not self.dummy_run:
            self.pwm.change_duty_cycle(pwm_power)
        pass

    def define_pwm_power(self, target_temp, read_temp, min_delta = -10, max_delta = 0):
        delta_temp = read_temp - target_temp
        
        if delta_temp < min_delta:
            delta_temp = min_delta
        elif delta_temp > max_delta:
            delta_temp = 0
        
        pwm_power = (max_delta - delta_temp) / (max_delta - min_delta)

        if not self.dummy_run:
            self.set_pwm_power(pwm_power)

        return pwm_power
