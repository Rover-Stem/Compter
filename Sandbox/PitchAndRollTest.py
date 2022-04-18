import numpy as np

def RotX (vector, degree):

	rot = np.asarray([[1, 0, 0], [0, np.cos(np.radians(degree)), (-1 * np.sin(np.radians(degree)))], [0, np.sin(np.radians(degree)), np.cos(np.radians(degree))]])
	return rot.dot(vector)

def RotY (vector, degree):

	rot = np.asarray([[np.cos(np.radians(degree)), 0, np.sin(np.radians(degree))], [0, 1, 0], [(-1 * np.sin(np.radians(degree))), 0, np.cos(np.radians(degree))]])
	return rot.dot(vector)

def RotZ (vector, degree):

	rot = np.asarray([[np.cos(np.radians(degree)), (-1 * np.sin(np.radians(degree))), 0], [np.sin(np.radians(degree)), np.cos(np.radians(degree)), 0], [0, 0, 1]])
	return rot.dot(vector)

def findPitch (vector):

	return np.degrees(np.arctan2(vector[0], np.sqrt(np.power(vector[1], 2) + np.power(vector[2], 2))))

def findRoll (vector):

	return np.degrees(np.arctan2(vector[1], np.sqrt(np.power(vector[0], 2) + np.power(vector[2], 2))))

g = np.asarray([[0], [0], [-9.82]])

roll10 = RotX(g, 10)
pitch20 = RotY(roll10, -20)

print(findPitch(pitch20))
print(findRoll(pitch20))