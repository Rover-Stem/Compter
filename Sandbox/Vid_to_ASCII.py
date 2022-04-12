import cv2
import time
import numpy as np
import matplotlib.pyplot as plt

def outputPic (x, y, output):

	min_size_x = 90

	# X = True, Y = False
	x_or_y = False

	gradient = ["█", "$", "@", "B", "%", "8", "&", "W", "M", "#", "*", "o", "a", "h", "k", "b", "d", "p", "q", "w", "m", "Z", "O", "0", "Q", "L", "C", "J", "U", "Y", "X", "z", "c", "v", "u", "n", "x", "r", "j", "f", "t", "/", "\\", "|", "(", ")", "1", "{", "}", "[", "]", "?", "-", "_", "+", "~", "<", ">", "i", "!", "l", "I", ";", ":", ",", "\"", "^", "`", "'", ".", " "]

	img_orig = cv2.imread(f'../../Animations/Waiting Term/All Frames/overlayed_x{x}_y{y}.png')
	img = cv2.cvtColor(img_orig, cv2.COLOR_BGR2GRAY)

	if (img.shape[1] > img.shape[0]):

		min_size = int(min_size_x / 2)
		x_or_y = True

	else:

		min_size = int(min_size_x / 2)
		x_or_y = False

	if (x_or_y):

		percent = min_size / img.shape[1]
		new_size = (min_size, int(img.shape[0] * percent))

	else:

		percent = min_size / img.shape[0]
		new_size = (int(img.shape[1] * percent), min_size)

	img_orig = cv2.resize(img_orig, new_size)
	img = cv2.resize(img, new_size)

	# (height, width)
	#print(img.shape)

	img = img * (70 / 255)

	final_ascii = [[]]
	final_rgb = [[]]

	for i in range(0, img.shape[0]):

		for j in range(0, img.shape[1]):

			#print(f"ASCII: {final_ascii}")
			#print(f"Color: {final_rgb}")
			#print(f"Luminence: {int(img[i][j])}\n")

			final_ascii[-1].append(gradient[70 - int(img[i][j])] + " ")
			final_rgb[-1].append([img_orig[i][j][0], img_orig[i][j][1], img_orig[i][j][2]])

		final_ascii.append([])
		final_rgb.append([])

	for i in range(0, len(final_ascii)):

		for j in range(0, len(final_ascii[i])):

			number = 16 + 36 * final_rgb[i][j][0] + 6 * final_rgb[i][j][1] + final_rgb[i][j][2]
			print(f"{final_ascii[i][j]}", end = "")

			if (output):

				with open("Animations/waitingTerm.animation", 'a') as f:

					f.write(f"{final_ascii[i][j]}")

		print()

		if (output):

			with open("Animations/waitingTerm.animation", 'a') as f:

				f.write("\n")

path = [(0, 1050), (2350, 1050), (2350, 500), (0, 500), (0, 1050)]
output = True
frameRate = 40

time = 0

for index in range((len(path) - 1)):

	xStart = path[index][0]
	xEnd = path[index + 1][0]

	yStart = path[index][1]
	yEnd = path[index + 1][1]

	timeX = np.abs(int(np.round(((xEnd - xStart) / 50) / frameRate)))
	timeY = np.abs(int(np.round(((yEnd - yStart) / 50) / frameRate)))

	if (timeX > timeY):

		if (timeX == 0):

			rateX = 0

		else:

			rateX = ((xEnd - xStart) / 50) / timeX

		if (timeY == 0):

			rateY = 0

		else:

			rateY = ((yEnd - yStart) / 50) / timeX

		for t in range(0, (timeX * frameRate)):

			time += (t / frameRate)

			if (output):

				with open("Animations/waitingTerm.animation", 'a') as f:

					f.write(f"{time}\n")

			outputPic(int(np.round(((rateX * (t / frameRate)))) * 50 + xStart), int(np.round(((rateY * (t / frameRate)))) * 50 + yStart), output)

	else:

		if (timeX == 0):

			rateX = 0

		else:

			rateX = ((xEnd - xStart) / 50) / timeY

		if (timeY == 0):

			rateY = 0

		else:

			rateY = ((yEnd - yStart) / 50) / timeY

		for t in range(0, (timeY * frameRate)):

			time += (t / frameRate)

			if (output):

				with open("Animations/waitingTerm.animation", 'a') as f:

					f.write(f"{time}\n")

			outputPic(int(np.round(((rateX * (t / frameRate)))) * 50 + xStart), int(np.round(((rateY * (t / frameRate)))) * 50 + yStart), output)