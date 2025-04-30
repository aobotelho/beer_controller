#include <OneWire.h>
#include <DallasTemperature.h>
#include <ArduinoJson.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h> // Biblioteca utilizada para fazer a comunicação com o display 20x4 

/*********************************************************************************************************************
*
* Definitions regarding OneWire communication (Temperature)
*
*********************************************************************************************************************/
// Data wire is conntec to the Arduino digital pin 4
#define ONE_WIRE_BUS 4

// Setup a oneWire instance to communicate with any OneWire devices
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

/*********************************************************************************************************************
*
* Definitions regarding OneWire communication (Temperature)
*
*********************************************************************************************************************/
#define LCD_COL 16 // Serve para definir o numero de colunas do display utilizado
#define LCD_ROW  2 // Serve para definir o numero de linhas do display utilizado
#define LCD_ADD  0x27 // Serve para definir o endereço do display.

LiquidCrystal_I2C lcd(LCD_ADD, LCD_COL, LCD_ROW); // Chamada da funcação LiquidCrystal para ser usada com o I2C



/*********************************************************************************************************************
*
* General definitions
*
*********************************************************************************************************************/
#define PWM_OUTPUT_PIN 6
#define TEMP_DIFF_LOWER_BOUND 0
#define TEMP_DIFF_UPPER_BOUND 4

/*********************************************************************************************************************
*
* General variables
*
*********************************************************************************************************************/
// Target temperature:
float target_temp = 65;

void setup(void){
    // Start serial communication for debugging purposes
    Serial.begin(9600);
    // Start up the library
    sensors.begin();

    pinMode(PWM_OUTPUT_PIN, OUTPUT); 
    pinMode(2, OUTPUT);
    digitalWrite(2, HIGH);

    lcd.init(); // Serve para iniciar a comunicação com o display já conectado
    lcd.backlight(); // Serve para ligar a luz do display
    lcd.clear(); // Serve para limpar a tela do display

    lcd.setCursor(1,0); 
    lcd.print("Hello");
    lcd.setCursor(1, 1);
    lcd.print("World!");
}

void loop(void){ 
    float pwm_duty_cycle = 0; 
    float current_temperature = 0;

    // Step 1: 
    process_temperature(&pwm_duty_cycle, &current_temperature, &target_temp);

    // Step 2:
    check_communication();


    Serial.print("- Celsius temperature: ");
    Serial.println(current_temperature);
    Serial.print("- Target temperature: ");
    Serial.println(target_temp);
    Serial.print("- PWM Duty Cycle: ");
    Serial.println(pwm_duty_cycle);
    Serial.println();

    lcd.setCursor(1,0); 
    lcd.print("Tgt tmp:");
    lcd.print(target_temp);
    lcd.setCursor(1, 1);
    lcd.print("Cur tmp:");
    lcd.print(current_temperature);
    delay(3000);
}

void check_communication(void){
    /*********************************************************************************************************************
    *
    * This function expects a JSON input from serial. 
    * The JSON is "the standard format": {"key":"value"}
    * Value may be a string or, when explicit, a number. 
    *
    * Example:
    *   For a new temperature it is expected the following KV format:
    *       {"new_temp":20}
    *       {"new_temp":20.0}
    *       {"new_temp":20.123}
    *
    *********************************************************************************************************************/
    JsonDocument json_communication_var;
    if (Serial.available() > 0) {
        deserializeJson(json_communication_var, Serial.readString());

        for (JsonPair key_value : json_communication_var.as<JsonObject>()) {
            if (key_value.key() == "new_temp"){
                target_temp = key_value.value().as<float>();
                Serial.print("\n\nNew target temp!!!!:");
                Serial.println(target_temp);
            }
            else{
                Serial.println("\n\n????? Found strange key value pair ????");
                Serial.print("Key: ");
                Serial.println(key_value.key().c_str());
                Serial.print("Value: ");
                Serial.println(key_value.value().as<const char*>());
            }
        }
    }
}

void process_temperature(float *var_pwm_duty_cycle, float *var_current_temperature, float *var_target_temp){
    // Call sensors.requestTemperatures() to issue a global temperature and Requests to all devices on the bus
    sensors.requestTemperatures(); 
    *var_current_temperature = sensors.getTempCByIndex(0);

    Serial.print("Temp error: ");
    Serial.println(*var_target_temp - *var_current_temperature);

    if(*var_target_temp - *var_current_temperature > TEMP_DIFF_UPPER_BOUND){
        *var_pwm_duty_cycle = 255;
    }
    else if (*var_target_temp - *var_current_temperature < TEMP_DIFF_LOWER_BOUND){
        *var_pwm_duty_cycle = 0;
    }
    else{
        *var_pwm_duty_cycle = 255 * (*var_target_temp - *var_current_temperature) / TEMP_DIFF_UPPER_BOUND;
    }

    analogWrite(PWM_OUTPUT_PIN, *var_pwm_duty_cycle);
}
