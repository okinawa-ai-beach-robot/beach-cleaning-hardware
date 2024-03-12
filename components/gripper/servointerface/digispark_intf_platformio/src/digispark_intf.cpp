#include <Arduino.h>

// Model: A
// LED on pin 1
// 5V IO! input 3v3 as high is fine!

/* This code reads a servo signal and starts to: 
 * - inflate on an pulse between 1500+250 to 1500+450 us
 * - deflate on an pulse between 1500-450 to 1500-250 us
 * - stop the current action between 1500-100 to 1500+100 us
 * - Error stop (same as stop so far) if signal is unexpected
 * 
 * Each stop signal requires a deflate signal first, as the gripper can be damages through an unexpected double inflation.
 * Servo signal is expected to be ~50Hz, no singla is interpreted as out of spec -> stop signal
 * 
 * Pin 0: PWM input (no pullup)
 * Pin 1: inflate motor
 * Pin 2: deflate motor
 * 
 * IO is 5v! anyway, pwm input from ESP is fine (3v3), but we can not send a signal to the esp (robot arm controller)
 */


#define PIN_PWM_IN 0
#define PIN_INFLATE_OUT 1
#define PIN_DEFLATE_OUT 2

#define T_DEFLATE 1000
#define T_INFLATE 700


enum Action
{
  DO_NOTHING=0,
  IS_DEFLATING=1,
  IS_INFLATING=2
};


unsigned long t_start_action;
unsigned long t_timeout;

Action current_action;
Action previous_action;

bool time_is_up(unsigned long ms)
{
  unsigned long t_now = millis();
  unsigned long dt = t_now - t_start_action;
  return dt>ms;
}

void time_is_now()
{
  t_start_action = millis();
}

void setup()
{
  pinMode(PIN_PWM_IN,INPUT);
  pinMode(PIN_INFLATE_OUT,OUTPUT);
  pinMode(PIN_DEFLATE_OUT,OUTPUT);
  t_start_action = 0;
  t_timeout = 0;

  digitalWrite(PIN_INFLATE_OUT, LOW);
  digitalWrite(PIN_DEFLATE_OUT, LOW);
  current_action = Action::DO_NOTHING;
  previous_action = Action::DO_NOTHING;
}

void loop() 
{
  // blocking for pulse -> 50Hz if connected! if 50ms passed return.. assume no connection:
  unsigned long duration = pulseIn(PIN_PWM_IN, HIGH, 50000);

  // avoid overflow:
  if (duration>2500) duration = 2500;

  // duration should be 1000-2000us!
  // Duration is now -500..500
  long ctrl_in = duration-1500;

  // detect binary events:
  if ((duration<-250)&&(duration>-450))
  {
    // Deflate!!
    if ((current_action == Action::DO_NOTHING) && (previous_action != Action::IS_DEFLATING))
    {
      digitalWrite(PIN_INFLATE_OUT, LOW);
      digitalWrite(PIN_DEFLATE_OUT, HIGH);
      time_is_now();
      t_timeout = T_DEFLATE;
      current_action = Action::IS_DEFLATING;
    }
  }
  else if ((duration>250) && (duration<450))
  {
    // Inflate!
    if ((current_action == Action::DO_NOTHING) && (previous_action != Action::IS_INFLATING))
    {
      digitalWrite(PIN_INFLATE_OUT, HIGH);
      digitalWrite(PIN_DEFLATE_OUT, LOW);
      time_is_now();
      t_timeout = T_INFLATE;
      current_action = Action::IS_INFLATING;
    }
  }
  else if ((duration>-100) && (duration<100))
  {
    // Stop!
    digitalWrite(PIN_INFLATE_OUT, LOW);
    digitalWrite(PIN_DEFLATE_OUT, LOW);
    // Not sure what happend but we should avoid double inflation (gripper could burst)!
    // So we pretend the gripper is inflated and must be deflated first!
    previous_action = Action::IS_INFLATING;
    current_action = Action::DO_NOTHING;
  }
  else
  {
    // Error ?!
    digitalWrite(PIN_INFLATE_OUT, LOW);
    digitalWrite(PIN_DEFLATE_OUT, LOW);
    // Not sure what happend but we should avoid double inflation (gripper could burst)!
    // So we pretend the gripper is inflated and must be deflated first!
    previous_action = Action::IS_INFLATING;
    current_action = Action::DO_NOTHING;
  }

  if ((current_action!=Action::DO_NOTHING) && (time_is_up(t_timeout)))
  {
    digitalWrite(PIN_INFLATE_OUT, LOW);
    digitalWrite(PIN_DEFLATE_OUT, LOW);
    previous_action = current_action;
    current_action = Action::DO_NOTHING;
  }



  //// Test IO (led)
  // digitalWrite(1,HIGH);
  // delay(500);
  // digitalWrite(1,LOW);
  // delay(200);
  // digitalWrite(1,HIGH);
  // delay(200);
  // digitalWrite(1,LOW);
  // delay(200);
 }
