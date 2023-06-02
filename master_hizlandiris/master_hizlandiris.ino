#include <Stepper.h>
#include <math.h>

///////////////////////////////////////
// MOTOR_1 --> LEFT
uint8_t MOTOR1_1 = 8;
uint8_t MOTOR1_2 = 9;
uint8_t MOTOR1_3 = 10;
uint8_t MOTOR1_4 = 11;

uint8_t MOTOR2_1 = 7;
uint8_t MOTOR2_2 = 6;
uint8_t MOTOR2_3 = 5;
uint8_t MOTOR2_4 = 4;
///////////////////////////////////////

const int steps_per_rev = 200;

Stepper MotorLeft(steps_per_rev, MOTOR1_1, MOTOR1_2, MOTOR1_3, MOTOR1_4);
Stepper MotorRight(steps_per_rev, MOTOR2_1, MOTOR2_2, MOTOR2_3, MOTOR2_4);

// speed / time arrays
float motor_left_arr[500] = {0};
int motor_left_arr_length = 0;
float motor_right_arr[500] = {0};
int motor_right_arr_length = 0;
float time_arr[500] = {0};
int time_arr_length = 0;

int current_index = 0;
auto millis_begin = millis();

int left_time_step_count = 1;
int right_time_step_count = 1;

void setup_wifi_module() {
  Serial1.begin(115200);
  Serial1.println("AT");
  while(!Serial1.find("OK")){
    Serial1.println("AT");
  }
  Serial1.println("AT+CWMODE=3");
  while(!Serial1.find("OK")){
    Serial1.println("AT+CWMODE=3");
  }
  Serial1.println("AT+CWLIF");
  while(!Serial1.find("192.168.4.2") and !Serial1.find("192.168.4.3")){
    Serial1.println("AT+CWLIF");
    Serial.println("Waiting for connection.");
  }
  Serial1.println("AT+CIPMUX=1");
  while(!Serial1.find("OK")){
    Serial1.println("AT+CIPMUX=1");
    Serial.println("Error.");
  }
  Serial1.println("AT+CIPSERVER=1,333");
  while(!Serial1.find("OK")){
    Serial1.println("AT+CIPSERVER=1,333");
    Serial.println("Error.");
  }
}

bool receive_from_gui() {
  // receive lin/ang velocities and time array

  // receive left
  Serial.println("receiving left");

  bool completed = false;
  while(!completed){
    while(!Serial1.find("+IPD"));
    Serial.println("Left chunk transfer began.");
    if (Serial1.find(":")) {
      byte buffer[400];
      Serial1.readBytes(buffer,400);
      for (int i = 0; i < 400; i += 4) {
        byte byteArray[4]; // Your byte array of size 4
        byteArray[0] = buffer[i+3];
        byteArray[1] = buffer[i+2];
        byteArray[2] = buffer[i+1];
        byteArray[3] = buffer[i];
        float floatValue;
        memcpy(&floatValue, byteArray, sizeof(float));
        if(floatValue < -990)
        {
          Serial.println("Left array completed.");
          Serial.println(motor_left_arr_length);
          completed = true;
          break;
        }
        else        
          motor_left_arr[motor_left_arr_length++] = floatValue;
      }
    }
  }
  
  // receive right
  Serial.println("receiving right");

  completed = false;
  while(!completed){
    while(!Serial1.find("+IPD"));
    Serial.println("Right chunk transfer began.");
    if (Serial1.find(":")) {
      byte buffer[400];
      Serial1.readBytes(buffer,400);
      for (int i = 0; i < 400; i += 4) {
        byte byteArray[4]; // Your byte array of size 4
        byteArray[0] = buffer[i+3];
        byteArray[1] = buffer[i+2];
        byteArray[2] = buffer[i+1];
        byteArray[3] = buffer[i];
        float floatValue;
        memcpy(&floatValue, byteArray, sizeof(float));
        if(floatValue < -990)
        {
          Serial.println("Right array completed.");
          Serial.println(motor_right_arr_length);
          completed = true;
          break;
        }
        else
          motor_right_arr[motor_right_arr_length++] = floatValue;          
      }
    }
  }
  
  // receive time
  Serial.println("receiving time");

  completed = false;
  while(!completed){
    while(!Serial1.find("+IPD"));
    Serial.println("Time chunk transfer began.");
    if (Serial1.find(":")) {
      byte buffer[400];
      Serial1.readBytes(buffer,400);
      for (int i = 0; i < 400; i += 4) {
        byte byteArray[4]; // Your byte array of size 4
        byteArray[0] = buffer[i+3];
        byteArray[1] = buffer[i+2];
        byteArray[2] = buffer[i+1];
        byteArray[3] = buffer[i];
        float floatValue;
        memcpy(&floatValue, byteArray, sizeof(float));
        if(floatValue < -990)
        {
          Serial.println("Time array completed.");
          Serial.println(time_arr_length);
          completed = true;
          break;
        }
        else
          time_arr[time_arr_length++] = floatValue;
      }
    }
  }

  if(completed)
    Serial.println("All the path data has been received!");

  return completed;
}

void stop_car()
{
    digitalWrite(MOTOR1_1, LOW);
    digitalWrite(MOTOR1_2, LOW);
    digitalWrite(MOTOR1_3, LOW);
    digitalWrite(MOTOR1_4, LOW);
    digitalWrite(MOTOR2_1, LOW);
    digitalWrite(MOTOR2_2, LOW);
    digitalWrite(MOTOR2_3, LOW);
    digitalWrite(MOTOR2_4, LOW);
}

void debug_print() {
  // debug
  Serial.println("printing left");
  for (int i = 0; i < motor_left_arr_length; i++) {
    Serial.print(i);
    Serial.print(": ");
    Serial.println(motor_left_arr[i]);
  }
  Serial.println("printing right");
  for (int i = 0; i < motor_right_arr_length; i++) {
    Serial.print(i);
    Serial.print(": ");
    Serial.println(motor_right_arr[i]);
  }
  Serial.println("printing time");
  for (int i = 0; i < time_arr_length; i++) {
    Serial.print(i);
    Serial.print(": ");
    Serial.println(time_arr[i]);
  }
}

void setup()
{
  Serial.begin(9600);

  setup_wifi_module();
  Serial.println("wifi set up");

  while(!receive_from_gui());

  //debug_print();

  MotorLeft.setSpeed(120);
  MotorRight.setSpeed(120);

  Serial.println("millis");
  millis_begin = millis();
}

void loop()
{
  // end
  if (current_index == time_arr_length - 2)
  {
    stop_car();
    return;
  }

  // advance to the next generation
  auto curr_time = millis() - millis_begin;
  if (curr_time > time_arr[current_index + 1])
  {
    current_index++;
    Serial.println("Arttiris");
    left_time_step_count = 1;
    right_time_step_count = 1;
  }

  auto time_interval = time_arr[current_index+1] - time_arr[current_index];

  // step left if the time has come
  curr_time = millis() - millis_begin;
  if (motor_left_arr[current_index] != 0)
  {
    if (curr_time - time_arr[current_index] >
    (time_interval / motor_left_arr[current_index]) * left_time_step_count )
    {
      if (left_time_step_count != abs(motor_left_arr[current_index]))
      {
        int step_dir = (motor_left_arr[current_index] > 0) ? 1 : -1;
        MotorLeft.step(step_dir);
        left_time_step_count++;
      }
    }
  }
  
  // step right if the time has come
  curr_time = millis() - millis_begin;
  if (motor_right_arr[current_index] != 0)
  {
    if (curr_time - time_arr[current_index] >
    (time_interval / motor_right_arr[current_index]) * right_time_step_count )
    {
      if (right_time_step_count != abs(motor_right_arr[current_index]))
      {
        int step_dir = (motor_right_arr[current_index] > 0) ? 1 : -1;
        MotorRight.step(step_dir);
        right_time_step_count++;
      }
    }
  }
}
