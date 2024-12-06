#include <SCServo.h>

#define SMS_STS_MAX_TORQUE 16
#define MAX_TORQUE_LIMIT   48
#define SET_MAX_TORQUE     250 // JFQ TODO

// === ST Servo === TypeNum:9
SMS_STS st;
float ServoDigitalRange_ST  = 4095.0;
float ServoAngleRange_ST    = 360.0;
float ServoDigitalMiddle_ST = 2047.0;
#define ServoInitACC_ST      100
#define ServoMaxSpeed_ST     4000
#define MaxSpeed_X_ST        4000
#define ServoInitSpeed_ST    2000

// === SC Servo === TypeNum:5 (used, e.g., for 2nd gripper!)
SCSCL sc;
float ServoDigitalRange_SC  = 1023.0;
float ServoAngleRange_SC    = 210.0;
float ServoDigitalMiddle_SC = 511.0;
#define ServoInitACC_SC      0
#define ServoMaxSpeed_SC     1500
#define MaxSpeed_X_SC        1500
#define ServoInitSpeed_SC    800
int MAX_MIN_OFFSET = 30;


bool ID_Stu[5] = {false, false, false, false, false};

// set serial feedback.
bool serialFeedback = true;
bool feedBackErrorCheck = false;

// set the servo ID list.
byte ID_List[253];
bool Torque_List[253];
int  ServoType[253];

// []: the ID of the servo.
// the buffer of the information read from the active servo.
s16  loadRead[253];
s16  speedRead[253];
byte voltageRead[253];
int  currentRead[253];
s16  posRead[253];
s16  modeRead[253];
s16  temperRead[253];

// []: the num of the active servo.
// use listID[activeNumInList] to get the ID of the active servo.
byte listID[253];
byte searchNum = 0;
bool searchedStatus = false;
bool searchFinished = false;
bool searchCmd      = false;
byte activeNumInList = 0;
s16 activeServoSpeed = 100;
byte servotoSet = 0;

bool doJ2MultiTurn=false;

// linkageBuffer to save the angle.
float linkageBuffer[50];

// the buffer of the bytes read from USB-C and servos. 
int usbRead;
int stsRead;


bool getFeedBack(byte servoID){
  if(ServoType[servoID]==9)
  {
    if(st.FeedBack(servoID)!=-1){
      posRead[servoID] = st.ReadPos(-1);
      speedRead[servoID] = st.ReadSpeed(-1);
      loadRead[servoID] = st.ReadLoad(-1);
      voltageRead[servoID] = st.ReadVoltage(-1);
      currentRead[servoID] = st.ReadCurrent(-1);
      temperRead[servoID] = st.ReadTemper(-1);
      modeRead[servoID] = st.ReadMode(servoID);
      feedBackErrorCheck = false;
      return true;
    }
    else{
      if(serialFeedback){
        Serial.println("FeedBack err 9");
        Serial.print("ID"); Serial.print(servoID); Serial.println(" ");
      }
      feedBackErrorCheck = true;
      return false;
    }
  }
  else  if(ServoType[servoID] == 5)
  {
    if(sc.FeedBack(servoID)!=-1){
      posRead[servoID] = sc.ReadPos(-1);
      speedRead[servoID] = sc.ReadSpeed(-1);
      loadRead[servoID] = sc.ReadLoad(-1);
      voltageRead[servoID] = sc.ReadVoltage(-1);
      currentRead[servoID] = sc.ReadCurrent(-1);
      temperRead[servoID] = sc.ReadTemper(-1);
      modeRead[servoID] = sc.ReadMode(servoID);
      feedBackErrorCheck = false;
      return true;
    }
    else{
      if(serialFeedback){
        Serial.println("FeedBack err 5");
        Serial.print("ID"); Serial.print(servoID); Serial.println(" ");
      }
      
    }

  }
  feedBackErrorCheck = true;
  return false;

}

void activateJ2MultiTurn(){

  // TODO
  doJ2MultiTurn = true;
}


void getFeedBackAll(){
  ID_Stu[0] = getFeedBack(1);
  ID_Stu[1] = getFeedBack(2);
  ID_Stu[2] = getFeedBack(3);
  ID_Stu[3] = getFeedBack(4);
  ID_Stu[4] = getFeedBack(5);
}


void servoInit(){
  Serial1.begin(1000000, SERIAL_8N1, S_RXD, S_TXD);
  st.pSerial = &Serial1;
  sc.pSerial = &Serial1;
  while(!Serial1) {}
  for (int i = 0; i < 6; i++){
    Torque_List[i] = true;
    ServoType[i]   = -1;


    // read servo type SC or ST types exist (original arm only uses ST)
    ServoType[i] = st.readByte(i, 3);

    Serial.print("Servotype: ");
    Serial.println(ServoType[i]);

    // if (ServoType[i]==9)
    // {
    //   st.EnableTorque(i, 1);
    // }
    // else if(ServoType[i]==5){
    //   sc.EnableTorque(i, 1);
    // }
  }
}


void setMiddle(byte InputID){
  if(ServoType[InputID]==9)
  {
    Serial.print(InputID); Serial.println(" middle set");
    st.CalibrationOfs(InputID);
    st.unLockEprom(InputID);
    st.writeWord(InputID, SMS_STS_MAX_TORQUE, SET_MAX_TORQUE);
    // TODO JFQ, necessary?:
    // SMS_STS_MAX_TORQUE is inital value loaded into MAX_TORQUE_LIMIT during power up
    st.writeWord(InputID, MAX_TORQUE_LIMIT, SET_MAX_TORQUE);
    st.LockEprom(InputID);
  }
  else if(ServoType[InputID] == 5)
  {
    Serial.println(" middle set servo 5");
    sc.unLockEprom(InputID);
    st.writeWord(InputID, SMS_STS_MAX_TORQUE, SET_MAX_TORQUE);
    st.LockEprom(InputID);
  }
  else{
    Serial.println(" middle set FAIL!!");
  }

}

void setMaxTorque(byte InputID, uint16_t percent_x10)
{
  if (percent_x10<=1000)
  {
      if(ServoType[InputID]==9)
      {
        st.writeWord(InputID, MAX_TORQUE_LIMIT, percent_x10);
        // TODO maybe SMS_STS_MAX_TORQUE register as well?
      }
      else if(ServoType[InputID] == 5)
      {
        st.writeWord(InputID, SMS_STS_MAX_TORQUE, percent_x10);
      }

  }


}

void setTargetJointAngle(uint8_t id, int16_t pos, uint16_t speed, uint8_t accel)
{
  if(ServoType[id] == 9)
  {
    // Serial.print("a");
    // Serial.println(id);
    // Serial.println(pos);
    // Serial.println(speed);
    // Serial.println(accel);
    st.WritePosEx(id, pos, speed, accel);
  }
  else if(ServoType[id] == 5)
  {
    // Serial.print("b");
    // Serial.println(id);
    sc.WritePosEx(id, pos, speed, accel);
  }
  else{
    Serial.print("can not move servo!");
  }

}


  // for (uint8_t i=0; i<5; i++)
  // {
  //   setTargetJointAngle(jsonID[i],jsonPosCtrl[i],jsonSpdCtrl[i],jsonAccCtrl[i]);
  // }


void setMode(byte InputID, byte InputMode){
  if(InputMode == 0){
    if(ServoType[InputID] == 9){
      st.unLockEprom(InputID);
      st.writeWord(InputID, 11, 4095);
      st.writeByte(InputID, SMS_STS_MODE, InputMode);
      st.LockEprom(InputID);
    }
    else if(ServoType[InputID] == 5){
      sc.unLockEprom(InputID);
      sc.writeWord(InputID, SCSCL_MIN_ANGLE_LIMIT_L, 20);
      sc.writeWord(InputID, SCSCL_MAX_ANGLE_LIMIT_L, 1003);
      sc.LockEprom(InputID);
    }
  }

  else if(InputMode == 3){
    if(ServoType[InputID] == 9){
      st.unLockEprom(InputID);
      st.writeByte(InputID, SMS_STS_MODE, InputMode);
      st.writeWord(InputID, 11, 0);
      st.LockEprom(InputID);
    }
    else if(ServoType[InputID] == 5){
      sc.unLockEprom(InputID);
      sc.writeWord(InputID, SCSCL_MIN_ANGLE_LIMIT_L, 0);
      sc.writeWord(InputID, SCSCL_MAX_ANGLE_LIMIT_L, 0);
      sc.LockEprom(InputID);
    }
  }
}


void setID(byte ID_select, byte ID_set){
  if(ServoType[ID_select] == 9){
    st.unLockEprom(ID_select);
    st.writeByte(ID_select, SMS_STS_ID, ID_set);
    st.LockEprom(ID_set);
  }
  else if(ServoType[ID_select] == 5){
    sc.unLockEprom(ID_select);
    sc.writeByte(ID_select, SCSCL_ID, ID_set);
    sc.LockEprom(ID_set);
  }
}


void servoStop(byte servoID){
  if(ServoType[servoID] == 9){
    st.EnableTorque(servoID, 0);
    delay(10);
    st.EnableTorque(servoID, 1);
  }
  else if(ServoType[servoID] == 5){
    sc.EnableTorque(servoID, 0);
    delay(10);
    sc.EnableTorque(servoID, 1);
  } 
}


void servoTorque(byte servoID, u8 enableCMD){
  if(ServoType[servoID] == 9){
    st.EnableTorque(servoID, enableCMD);
  }
  else if(ServoType[servoID] == 5){
    sc.EnableTorque(servoID, enableCMD);
  }
}




void emergencyStopProcessing(){
  for (uint8_t sid = 1; sid<6; sid++)
  {
    servoTorque(sid, 0);
  }
  for(int i=0; i<10; i++){
    RGBcolor(255,25,0);
    delay(500);
    RGBcolor(0,0,0);
    delay(500);
  }
  for (uint8_t sid = 0; sid<6; sid++)
  {
    servoTorque(sid, 1);
  }
}

