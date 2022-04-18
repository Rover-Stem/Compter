import numpy as np
import pandas as pd

from matplotlib import pyplot as plt

def rotX (vector, rads):

	rot = np.asarray([[1, 0, 0], [0, np.cos(rads), (-1 * np.sin(rads))], [0, np.sin(rads), np.cos(rads)]])
	return rot.dot(vector)

def rotY (vector, rads):

	rot = np.asarray([[np.cos(rads), 0, np.sin(rads)], [0, 1, 0], [(-1 * np.sin(rads)), 0, np.cos(rads)]])
	return rot.dot(vector)

def rotZ (vector, rads):

	rot = np.asarray([[np.cos(rads), (-1 * np.sin(rads)), 0], [np.sin(rads), np.cos(rads), 0], [0, 0, 1]])
	return rot.dot(vector)

def findHeading (vector):

	if (vector[1] > 0):

		heading = (np.pi / 2) - np.arctan(vector[0] / vector[1])

	elif (vector[1] < 0):

		heading = ((3 * np.pi) / 2) - np.arctan(vector[0] / vector[1])

	else:

		if (vector[0] < 0):

			heading = np.pi

		else:

			heading = 0

	return heading

def findPitch (vector):

	return np.arctan2(vector[0], np.sqrt(np.power(vector[1], 2) + np.power(vector[2], 2)))

def findRoll (vector):

	return np.arctan2(vector[1], np.sqrt(np.power(vector[0], 2) + np.power(vector[2], 2)))

def findVelocity (vector, pitch, roll, yaw, dt):

	# Correct Vector

	vectCorrX = rotX(vector, (-1 * roll))
	vectCorrY = rotY(vectCorrX, (-1 * pitch))
	vectCorrZ = rotZ(vectCorrY, (-1 * yaw))
	vectCorrZ = np.asarray([vectCorrZ[0], vectCorrZ[1], 0])

	return vectCorrZ * dt

pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 1000)

data = pd.read_csv("04-18-2022--01:39:35.sim")

smoothData = data.apply(lambda x: np.convolve(x, np.ones((50, )) / 50, mode = 'same') if ((x.name == "MagX") or (x.name == "MagY") or (x.name == "MagZ") or (x.name == "AccelX") or (x.name == "AccelY") or (x.name == "AccelX")) else x)

analyzedData = pd.DataFrame(columns = ["Time Since Start", "Heading Raw", "Heading Smoothed", "Velocity Raw", "Velocity Smoothed", "Position Raw", "Position Smoothed"])

for i in range(len(data)):

	magRaw = np.asarray([data.loc[i, "MagX"], data.loc[i, "MagY"], data.loc[i, "MagZ"]])
	magSmooth = np.asarray([smoothData.loc[i, "MagX"], smoothData.loc[i, "MagY"], smoothData.loc[i, "MagZ"]])

	accRaw = np.asarray([data.loc[i, "AccX"], data.loc[i, "AccY"], data.loc[i, "AccZ"]])
	accSmooth = np.asarray([smoothData.loc[i, "AccX"], smoothData.loc[i, "AccY"], smoothData.loc[i, "AccZ"]])

	headingRaw = findHeading(magRaw)
	headingSmooth = findHeading(magSmooth)

	if (i == 0):

		velocityRaw = np.asarray([0, 0, 0])
		velocitySmooth = np.asarray([0, 0, 0])

		positionRaw = np.asarray([0, 0, 0])
		positionSmooth = np.asarray([0, 0, 0])

	else:

		dt = data.loc[i, "Time Since Start"] - data.loc[(i - 1), "Time Since Start"]

		velocityRaw = analyzedData.loc[(i - 1), "Velocity Raw"] + findVelocity(accRaw, findPitch(accRaw), findRoll(accRaw), headingRaw, dt)
		velocitySmooth = analyzedData.loc[(i - 1), "Velocity Smoothed"] + findVelocity(accSmooth, findPitch(accSmooth), findRoll(accSmooth), headingSmooth, dt)

		positionRaw = analyzedData.loc[(i - 1), "Position Raw"] + (velocityRaw * dt)
		positionSmooth = analyzedData.loc[(i - 1), "Position Smoothed"] + (velocitySmooth * dt)

	analyzedData.loc[len(analyzedData)] = [data.loc[i, "Time Since Start"], np.degrees(headingRaw), np.degrees(headingSmooth), velocityRaw, velocitySmooth, positionRaw, positionSmooth]

xRaw = [x[0] for x in analyzedData["Position Raw"].tolist()] * 1000
yRaw = [x[1] for x in analyzedData["Position Raw"].tolist()] * 1000

xSmoothed = [x[0] for x in analyzedData["Position Smoothed"].tolist()] * 1000
ySmoothed = [x[1] for x in analyzedData["Position Smoothed"].tolist()] * 1000

plt.plot(xRaw, yRaw, 'b')
plt.plot(xSmoothed, ySmoothed, 'g')
plt.xlabel("X (mm)")
plt.ylabel("Y (mm)")
plt.show()

time = analyzedData["Time Since Start"].to_list()

headingsRaw = analyzedData["Heading Raw"].to_list()
headingsSmoothed = analyzedData["Heading Smoothed"].to_list()

plt.plot(time, headingsRaw, 'b', label = "Raw Data")
plt.plot(time, headingsSmoothed, 'g', label = "Smoothed Data")
plt.legend(loc = 'upper left')
plt.xlabel("Time (sec)")
plt.ylabel("Degrees Heading")
plt.show()

