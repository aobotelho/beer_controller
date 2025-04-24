#include <OneWire.h>
#include <DallasTemperature.h>

// Data wire is conntec to the Arduino digital pin 4
#define ONE_WIRE_BUS 4

// Target temperature:
#define TARGET_TEMP 65

// Setup a oneWire instance to communicate with any OneWire devices
OneWire oneWire(ONE_WIRE_BUS);

// Pass our oneWire reference to Dallas Temperature sensor 
DallasTemperature sensors(&oneWire);

int pwm_output = 6; 

void setup(void){
  // Start serial communication for debugging purposes
  Serial.begin(9600);
  // Start up the library
  sensors.begin();

  pinMode(pwm_output, OUTPUT); 
}

void loop(void){ 
    float pwm_duty_cycle = 0; 
    float current_temperature = 0;


    // Call sensors.requestTemperatures() to issue a global temperature and Requests to all devices on the bus
    sensors.requestTemperatures(); 
    current_temperature = sensors.getTempCByIndex(0);

    Serial.println(TARGET_TEMP - current_temperature); 

    if(TARGET_TEMP - current_temperature > 4){
        pwm_duty_cycle = 255;
    }
    else if (TARGET_TEMP - current_temperature < 0){
        pwm_duty_cycle = 0;
    }
    else{
        pwm_duty_cycle = 255 * (TARGET_TEMP - current_temperature) / 4;
    }
    analogWrite(pwm_output,pwm_duty_cycle);

    Serial.print("Celsius temperature: ");
    Serial.println(current_temperature);
    Serial.print("PWM Duty Cycle: ");
    Serial.println(pwm_duty_cycle);
    delay(3000);
}


// void setup(void){
//   // Start serial communication for debugging purposes
//   Serial.begin(9600);
//   // Start up the library
//   sensors.begin();

//   pinMode(pwm_output, OUTPUT); 
// }

// void loop(void){ 
//     analogWrite(pwm_output,0);
//     Serial.println("0");
//     delay(3000); 
//     analogWrite(pwm_output,25);
//     Serial.println("25");
//     delay(3000); 
//     analogWrite(pwm_output,50);
//     Serial.println("50");
//     delay(3000); 
//     analogWrite(pwm_output,75);
//     Serial.println("75");
//     delay(3000); 
//     analogWrite(pwm_output,100);
//     Serial.println("100");
//     delay(3000); 
//     analogWrite(pwm_output,125);
//     Serial.println("125");
//     delay(3000); 
//     analogWrite(pwm_output,150);
//     Serial.println("150");
//     delay(3000);
//     analogWrite(pwm_output,175);
//     Serial.println("175");
//     delay(3000); 
//     analogWrite(pwm_output,200);
//     Serial.println("200");
//     delay(3000); 
//     analogWrite(pwm_output,225);
//     Serial.println("225");
//     delay(3000); 
//     analogWrite(pwm_output,250);
//     Serial.println("250");
//     delay(5000);
    
// }