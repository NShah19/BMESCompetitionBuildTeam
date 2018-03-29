#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

// The two BNO055 modules, bnoB has the ADR pin wired to 3.3v to change its i2c address
// Both are wired: SCL to analog 5, SDA to analog 4, VIN to 5v, GRN to ground
Adafruit_BNO055 bnoA = Adafruit_BNO055(-1, BNO055_ADDRESS_A);
Adafruit_BNO055 bnoB = Adafruit_BNO055(-1, BNO055_ADDRESS_B);
bool calibrated = false;

void setup() {
   Serial.begin(115200);
   if(!bnoA.begin()) {
       Serial.print("Ooops, BNO055(A) not detected");
   }
   bnoA.setExtCrystalUse(true);
   if(!bnoB.begin()) {
       Serial.print("Ooops, BNO055(B) not detected");
   }
   bnoB.setExtCrystalUse(true);
}

bool calibrateSensors(Adafruit_BNO055 bnoA, Adafruit_BNO055 bnoB)
{
  uint8_t sysA, gyroA, accelA, magA;
  sysA = gyroA = accelA = magA = 0;
  uint8_t sysB, gyroB, accelB, magB;
  sysB = gyroB = accelB = magB = 0;
  while(!(sysA == 3 && gyroA == 3 && accelA == 3 && magA == 3 && sysB == 3 && gyroB == 3 && accelB == 3 && magB == 3))
  {
    bnoA.getCalibration(&sysA, &gyroA, &accelA, &magA);
    bnoB.getCalibration(&sysB, &gyroB, &accelB, &magB);
    Serial.print("A calibration: ");
    displayCalStatus(bnoA);
    Serial.print("B calibration: ");
    displayCalStatus(bnoB);
    delay(1000);
  }
 return true;
}

void displayCalStatus(Adafruit_BNO055 bno)
{
  /* Get the four calibration values (0..3) */
  /* Any sensor data reporting 0 should be ignored, */
  /* 3 means 'fully calibrated" */
  uint8_t sys, gyro, accel, mag;
  sys = gyro = accel = mag = 0;
  bno.getCalibration(&sys, &gyro, &accel, &mag);
 
  /* The data should be ignored until the system calibration is > 0 */
  Serial.print("\t");
  if (!sys)
  {
    Serial.print("! ");
  }
 
  /* Display the individual values */
  Serial.print("Sys:");
  Serial.print(sys, DEC);
  Serial.print(" G:");
  Serial.print(gyro, DEC);
  Serial.print(" A:");
  Serial.print(accel, DEC);
  Serial.print(" M:");
  Serial.println(mag, DEC);
}

void loop() {
   if (!calibrated)
    calibrated = calibrateSensors(bnoA,bnoB);
   
   imu::Quaternion quatA = bnoA.getQuat();
   imu::Quaternion quatB = bnoB.getQuat();

   imu::Matrix<3> rot_matA = quatA.toMatrix();
   imu::Matrix<3> rot_matB = quatB.toMatrix();
    
   delay(500);
   /*
   Serial.print("qW: ");
   Serial.print(quatA.w(), 4);
   Serial.print(" qX: ");
   Serial.print(quatA.y(), 4);
   Serial.print(" qY: ");
   Serial.print(quatA.x(), 4);
   Serial.print(" qZ: ");
   Serial.print(quatA.z(), 4);
   Serial.println("");

   Serial.print("qW: ");
   Serial.print(quatB.w(), 4);
   Serial.print(" qX: ");
   Serial.print(quatB.y(), 4);
   Serial.print(" qY: ");
   Serial.print(quatB.x(), 4);
   Serial.print(" qZ: ");
   Serial.print(quatB.z(), 4);
   Serial.println("");
   delay(500); */
   
}
