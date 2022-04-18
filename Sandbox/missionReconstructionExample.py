from matplotlib import pyplot as plt
import datetime as dt
import numpy as np
import time
import csv

g = np.asarray([0, 0, 9.82])
times = []
accel = []
gyro = []
mag = []

with open('clean_data.csv', newline = '\n') as csvfile:

	Data = csv.DictReader(csvfile)

	for row in Data:

		times.append(row["Timestamp (UTC)"])
		accel.append(np.asarray([row["Accel-X"], row["Accel-Y"], row["Accel-Z"]]))
		gyro.append(np.asarray([row["Gyro-X"], row["Gyro-Y"], row["Gyro-Z"]]))
		mag.append(np.asarray([row["Mag-X"], row["Mag-Y"], row["Mag-Z"]]))

times = [dt.datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f') for x in times]
accel = np.asarray(accel).astype(np.float64)
gyro = np.asarray(gyro).astype(np.float64)
mag = np.asarray(mag).astype(np.float64)


print(f"1.) Mean Acceleration Z: {np.mean([item[2] for item in accel])}")
print(f"2.) Median Acceleration Z: {np.median([item[2] for item in accel])}")
print(f"3.) Mean Acceleration Magnitude: {np.mean([np.sqrt(x.dot(x)) for x in accel])}")
print(f"4.) Median Acceleration Magnitude: {np.median([np.sqrt(x.dot(x)) for x in accel])}")
print(f"5.) Mean Tilt Between IMU and true G: {np.mean([np.arccos((x.dot(g)) / (np.sqrt(x.dot(x)) * np.sqrt(g.dot(g)))) for x in accel])}")
print(f"6.) Median Tilt Between IMU and true G: {np.median([np.arccos((x.dot(g)) / (np.sqrt(x.dot(x)) * np.sqrt(g.dot(g)))) for x in accel])}")

v_x = [0] * len(accel)
v_y = [0] * len(accel)
x = [0] * len(accel)
y = [0] * len(accel)

for i in range(1, len(accel)):

	v_x[i] = v_x[i - 1] + accel[i][0] * ((times[i] - times[i - 1]).total_seconds())
	v_y[i] = v_y[i - 1] + accel[i][1] * ((times[i] - times[i - 1]).total_seconds())

for i in range(1, len(accel)):

	x[i] = x[i - 1] + v_x[i] * ((times[i] - times[i - 1]).total_seconds())
	y[i] = y[i - 1] + v_y[i] * ((times[i] - times[i - 1]).total_seconds())

print(f"7.) Integrated X Value: {x[-1]}")
print(f"8.) Integrated Y Value: {y[-1]}")

plt.plot(x, y, 'b')
plt.xlabel("X (m)")
plt.ylabel("Y (m)")
plt.show()

headings_smoothed = []
headings = []

Hx_list = np.convolve([item[0] for item in mag], np.ones((50, )) / 50, mode = 'same')
Hy_list = np.convolve([item[1] for item in mag], np.ones((50, )) / 50, mode = 'same')

for i in range(0, len(mag)):

	Hx = Hx_list[i]
	Hy = Hy_list[i]

	if Hy > 0:

		val = 90 - np.degrees(np.arctan(Hx / Hy))

	elif Hy < 0:

		val = 270 - np.degrees(np.arctan(Hx / Hy))

	else:

		if Hx < 0:

			val = 180

		else:

			val = 0

	headings_smoothed.append(val)

for i in range(0, len(mag)):

	Hx = mag[i][0]
	Hy = mag[i][1]

	if Hy > 0:

		val = 90 - np.degrees(np.arctan(Hx / Hy))

	elif Hy < 0:

		val = 270 - np.degrees(np.arctan(Hx / Hy))

	else:

		if Hx < 0:

			val = 180

		else:

			val = 0

	headings.append(val)

plt.plot(headings, 'b', label = "Non-Smoothed Data")
plt.plot(headings_smoothed, 'g', label = "Smoothed Data")
plt.legend(loc = 'upper left')
plt.xlabel("Time (sec)")
plt.ylabel("Degrees Heading")
plt.show()

print(f"11a.)\n\tX: {np.mean([item[0] for item in gyro])}\n\tY: {np.mean([item[1] for item in gyro])}\n\tZ: {np.mean([item[2] for item in gyro])}")
print(f"11b.)\n\tX: {np.median([item[0] for item in gyro])}\n\tY: {np.median([item[1] for item in gyro])}\n\tZ: {np.median([item[2] for item in gyro])}")

gyro_smoothed_x = np.convolve([item[0] for item in gyro], np.ones((50, )) / 50, mode = 'same')
gyro_smoothed_y = np.convolve([item[1] for item in gyro], np.ones((50, )) / 50, mode = 'same')
gyro_smoothed_z = np.convolve([item[2] for item in gyro], np.ones((50, )) / 50, mode = 'same')

plt.plot([item[0] for item in gyro], 'b', label = "X")
plt.plot([item[1] for item in gyro], 'r', label = "Y")
plt.plot([item[2] for item in gyro], 'g', label = "Z")
plt.plot(gyro_smoothed_x, 'black', label = "Smoothed X")
plt.plot(gyro_smoothed_y, 'maroon', label = "Smoothed Y")
plt.plot(gyro_smoothed_z, 'lime', label = "Smoothed Z")
plt.legend(loc = 'upper left')
plt.xlabel("Time (sec)")
plt.ylabel("RPM")
plt.show()

