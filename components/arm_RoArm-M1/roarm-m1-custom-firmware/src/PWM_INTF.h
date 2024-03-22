

#include <ESP32_Servo.h> 


#define PWM_PIN    23
Servo servo;



void InitPwmIo()
{
    servo.attach(PWM_PIN);
    servo.writeMicroseconds(1500);
}

void setPwmVal(uint16_t val)
{
    servo.writeMicroseconds(val);
}