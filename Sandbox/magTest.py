import board
import numpy as np
import adafruit_lsm303_accel
import adafruit_lsm303dlh_mag

i2c = board.I2C()
mag = adafruit_lsm303dlh_mag.LSM303DLH_Mag(i2c)
accel = adafruit_lsm303_accel.LSM303_Accel(i2c)

magRead = mag.magnetic
accRead = accel.acceleration

roll = np.arctan2(accRead[1], np.sqrt(np.power(accRead[0], 2) + np.power(accRead[2], 2)))
pitch = np.arctan2(accRead[0], np.sqrt(np.power(accRead[1], 2) + np.power(accRead[2], 2)))

magX = (magRead[0] * np.cos(pitch)) + (magRead[1] * np.sin(roll) * np.sin(pitch)) + (magRead[2] * np.cos(roll) * np.sin(pitch))
magY = (magRead[1] * np.cos(roll)) - (magRead[2] * np.sin(roll))
yaw = np.arctan2((-1 * magY), magX)

print(f"Pitch: {np.degrees(pitch)}")
print(f"Roll: {np.degrees(roll)}")
print(f"Yaw: {np.degrees(yaw)}")