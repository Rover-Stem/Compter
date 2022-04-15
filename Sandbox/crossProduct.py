import numpy as np

desiredAngle = 40 * (np.pi / 180)
currentAngle = 180 * (np.pi / 180)

print(f"Current Angle Vector: <{np.cos(currentAngle)}, {np.sin(currentAngle)}>\nDesired Angle Vector: <{np.cos(desiredAngle)}, {np.sin(desiredAngle)}>\nCross Product: {np.cross((np.cos(currentAngle), np.sin(currentAngle)), (np.cos(desiredAngle), np.sin(desiredAngle)))}")