import os
import glob
import time
from RPLCD import CharLCD

lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[33, 31, 29, 23])

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

#CELSIUS CALCULATION
def read_temp_c():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = int(temp_string) / 1000.0 # TEMP_STRING IS THE SENSOR OUTPUT, MAKE SURE IT'S AN INTEGER TO DO THE MATH
        temp_c = str(round(temp_c, 1)) # ROUND THE RESULT TO 1 PLACE AFTER THE DECIMAL, THEN CONVERT IT TO A STRING
        return temp_c

#FAHRENHEIT CALCULATION
def read_temp_f():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_f = (int(temp_string) / 1000.0) * 9.0 / 5.0 + 32.0 # TEMP_STRING IS THE SENSOR OUTPUT, MAKE SURE IT'S AN INTEGER TO DO THE MATH
        temp_f = str(round(temp_f, 1)) # ROUND THE RESULT TO 1 PLACE AFTER THE DECIMAL, THEN CONVERT IT TO A STRING
        return temp_f

void setup(void)
{
  lcd.init();                       // initialize the lcd
  lcd.backlight();
  Serial.begin(9600)
  sensors.begin();                  // turn on sensors for DS18b20
  pinMode(buttonUp, INPUT);         // Set INCREASE button to input
  pinMode(buttonDown, INPUT);       // Set DECREASE button to input
  lcd.setCursor(0,0);               // Set LCD cursor to first cursor spot
  lcd.print("Temperature");         // Print "Temperature" to cursor spot on LCD
}
void loop(void)
{

  sensors.requestTemperatures();    // Get temperature readings

  lcd.setCursor(2,1);
  lcd.print(sensors.getTempFByIndex(0));  // Print actual temperature

  // Write to Serial for Testing
  Serial.println("Actual Temperature");
  Serial.println(sensors.getTempFByIndex(0));

  // Increase target temp
  if (digitalRead(buttonUp) == HIGH) {
      targetTemp = ++targetTemp;     // If button is pushed, move Target Temp up by 1
    } else {
  }

  // Decrease target temp
  if (digitalRead(buttonDown) == HIGH) {
      targetTemp = --targetTemp;    // If button is pushed, move Target Temp down by 1
    } else {
  }

  Serial.println("Target Temperature");
  Serial.println(targetTemp);


while True:

    lcd.cursor_pos = (0, 0)
    lcd.write_string("Temp: " + read_temp_c() + unichr(223) + "C")
    lcd.cursor_pos = (1, 0)
    lcd.write_string("Temp: " + read_temp_f() + unichr(223) + "F")
