#include <Wire.h>
#include <EEPROM.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>
#include <Math.h>
// The two BNO055 modules, bnoB has the ADR pin wired to 3.3v to change its i2c address
// Both are wired: SCL to analog 5, SDA to analog 4, VIN to 5v, GRN to ground
Adafruit_BNO055 bnoA = Adafruit_BNO055(-1, BNO055_ADDRESS_A);
Adafruit_BNO055 bnoB = Adafruit_BNO055(-1, BNO055_ADDRESS_B);
bool calibrated = false;
double angleThreshold = 2.0;

bool calibrateSensors(Adafruit_BNO055 bnoA, Adafruit_BNO055 bnoB)
{
    uint8_t sysA, gyroA, accelA, magA;
    sysA = gyroA = accelA = magA = 0;
    uint8_t sysB, gyroB, accelB, magB;
    sysB = gyroB = accelB = magB = 0;
    while(!bnoA.isFullyCalibrated() || !bnoB.isFullyCalibrated())
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

void displaySensorOffsets(const adafruit_bno055_offsets_t &calibData)
{
    Serial.print("Accelerometer: ");
    Serial.print(calibData.accel_offset_x); Serial.print(" ");
    Serial.print(calibData.accel_offset_y); Serial.print(" ");
    Serial.print(calibData.accel_offset_z); Serial.print(" ");

    Serial.print("\nGyro: ");
    Serial.print(calibData.gyro_offset_x); Serial.print(" ");
    Serial.print(calibData.gyro_offset_y); Serial.print(" ");
    Serial.print(calibData.gyro_offset_z); Serial.print(" ");

    Serial.print("\nMag: ");
    Serial.print(calibData.mag_offset_x); Serial.print(" ");
    Serial.print(calibData.mag_offset_y); Serial.print(" ");
    Serial.print(calibData.mag_offset_z); Serial.print(" ");

    Serial.print("\nAccel Radius: ");
    Serial.print(calibData.accel_radius);

    Serial.print("\nMag Radius: ");
    Serial.print(calibData.mag_radius);
}

//-------------------------------------------------------------------
//TO DO: find the angle given two roation matrices between the x axis
//-------------------------------------------------------------------

double angleBetweenX( imu::Matrix<3> rot_matA,imu::Matrix<3> rot_matB)
{
  imu::Vector<3> firstXaxis = rot_matA.col_to_vector(0);
  imu::Vector<3> secondXaxis = rot_matB.col_to_vector(0);
  double dot_prod = firstXaxis.dot(secondXaxis);
  return acos(dot_prod)*180.0/3.14159;
}

double angleBetweenY( imu::Matrix<3> rot_matA,imu::Matrix<3> rot_matB)
{
  imu::Vector<3> firstYaxis = rot_matA.col_to_vector(1);
  imu::Vector<3> secondYaxis = rot_matB.col_to_vector(1);
  double dot_prod = firstYaxis.dot(secondYaxis);
  return acos(dot_prod)*180.0/3.14159;
}

double angleBetweenZ( imu::Matrix<3> rot_matA,imu::Matrix<3> rot_matB)
{
  imu::Vector<3> firstZaxis = rot_matA.col_to_vector(2);
  imu::Vector<3> secondZaxis = rot_matB.col_to_vector(2);
  double dot_prod = firstZaxis.dot(secondZaxis);
  return acos(dot_prod)*180.0/3.14159;
}

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
   /*
   if (!calibrated)
    calibrated = calibrateSensors(bnoA,bnoB);
   adafruit_bno055_offsets_t newCalib;
   bnoA.getSensorOffsets(newCalib);
   displaySensorOffsets(newCalib);
   bnoB.getSensorOffsets(newCalib);
   displaySensorOffsets(newCalib);
   */
}

void loop() {
   
   imu::Quaternion quatA = bnoA.getQuat();
   imu::Quaternion quatB = bnoB.getQuat();

   imu::Matrix<3> rot_matA = quatA.toMatrix();
   imu::Matrix<3> rot_matB = quatB.toMatrix();
   double output_list[] = {quatA.w(),quatA.x(),quatA.y(),quatA.z()};
   Serial.write(output_list, 4);
   delay(500);
}
