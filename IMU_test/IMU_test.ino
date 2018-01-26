
/*************************************************** 
  This is an example for the Adafruit Triple-Axis Gyro sensor

  Designed specifically to work with the Adafruit L3GD20 Breakout 
  ----> https://www.adafruit.com/products/1032

  These sensors use I2C or SPI to communicate, 2 pins (I2C) 
  or 4 pins (SPI) are required to interface.

  Adafruit invests time and resources providing this open source code, 
  please support Adafruit and open-source hardware by purchasing 
  products from Adafruit!

  Written by Kevin "KTOWN" Townsend for Adafruit Industries.  
  BSD license, all text above must be included in any redistribution
 ****************************************************/

#include <Wire.h> 
#include <Adafruit_L3GD20.h>
#include <Filters.h>
#include <Math.h>
const int xInput = A2;
const int yInput = A1;
const int zInput = A0;
const float zeropoint = 1.5; // voltage where 0g of force

/**************************/
FilterOnePole lowpassFilterx( LOWPASS, 100);  
FilterOnePole lowpassFiltery( LOWPASS, 100);  
FilterOnePole lowpassFilterz( LOWPASS, 25 );
float gacc[3];//index 0 is x, 1 is y, 2 is z
float Racc[3];
float Rmag = 1;
float Rest[3];
/******************************************/


// Comment this next line to use SPI
//#define USE_I2C

#ifdef USE_I2C
  // The default constructor uses I2C
  Adafruit_L3GD20 gyro;
#else
  // To use SPI, you have to define the pins
  #define GYRO_CS 5 // labeled CS
  #define GYRO_DO 6 // labeled SA0
  #define GYRO_DI 9  // labeled SDA
  #define GYRO_CLK 10 // labeled SCL
  Adafruit_L3GD20 gyro(GYRO_CS, GYRO_DO, GYRO_DI, GYRO_CLK);
#endif

void setup() 
{
  analogReference(EXTERNAL);
  Serial.begin(9600);
  Serial.print("y");
  // Try to initialise and warn if we couldn't detect the chip
   if (!gyro.begin(GYRO_RANGE_250DPS))
  //if (!gyro.begin(gyro.L3DS20_RANGE_500DPS))
  //if (!gyro.begin(gyro.L3DS20_RANGE_2000DPS))
  {
    Serial.println("Oops ... unable to initialize the L3GD20. Check your wiring!");
    while (1);
  }
}

void loop() 
{
  gyro.read();
  float xRaw = lowpassFilterx.input(analogRead(xInput));
  float yRaw = lowpassFiltery.input(analogRead(yInput));
  float zRaw = lowpassFilterz.input(analogRead(zInput));//these values a low pass filtered adc values we want convert to voltage so
  gacc[0] = ((xRaw*3/1023)-zeropoint)/.3;    //these values are delta volts - volts from the center voltage that counts as 0g.
  gacc[1] = ((yRaw*3/1023)-zeropoint)/.3;
  gacc[2] = ((zRaw*3/1023)-zeropoint)/.3;
  Rmag = sqrt(square(gacc[0])+square(gacc[1])+square(gacc[2]));//magnitude of force vector
  Rest[0] = gacc[0];
  Rest[1] = gacc[1];
  Rest[2] = gacc[2];
  Serial.print("Xang: "); Serial.print((int)gyro.data.x);   Serial.print(" ");
  Serial.print("Yang: "); Serial.print((int)gyro.data.y);   Serial.print(" ");
  Serial.print("Zang: "); Serial.println((int)gyro.data.z); Serial.print(" ");
  Serial.print("Xacc: "); Serial.print(gacc[0]); Serial.print(" ");
  Serial.print("Yacc: "); Serial.print(gacc[1]); Serial.print(" ");
  Serial.print("Zacc: "); Serial.print(gacc[2]); Serial.print(" ");
  delay(10);
}
