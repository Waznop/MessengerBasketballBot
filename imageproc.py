import numpy as np
import cv2

ballLo = np.array([0, 92, 231])
ballHi = np.array([48, 171, 255])
ringLo = np.array([15, 38, 255])
ringHi = np.array([15, 38, 255])

def findCenter(image):
	Y, X = image.shape
	m = image == 255
	total = np.sum(m)
	if total == 0:
		return -1, -1
	m = m / total
	# marginal distributions
	dx = np.sum(m, 0)
	dy = np.sum(m, 1)
	# expected values
	cx = int(np.sum(dx * np.arange(X)))
	cy = int(np.sum(dy * np.arange(Y)))
	return cx, cy

def getBallMask(image):
	return cv2.inRange(image, ballLo, ballHi)

def getRingMask(image):
	return cv2.inRange(image, ringLo, ringHi)

def getInfo(file1, file2, file3):
	image1 = cv2.imread(file1)
	image2 = cv2.imread(file2)
	image3 = cv2.imread(file3)

	ball = getBallMask(image1)
	bx, by = findCenter(ball)
	if bx == -1:
		ball = getBallMask(image2)
		bx, by = findCenter(ball)
	if bx == -1:
		ball = getBallMask(image3)
		bx, by = findCenter(ball)

	ring1 = getRingMask(image1)
	ring2 = getRingMask(image2)
	ring3 = getRingMask(image3)

	rx1, ry1 = findCenter(ring1)
	rx2, ry2 = findCenter(ring2)
	rx3, ry3 = findCenter(ring3)
	return bx, by, rx1, ry1, rx2, ry2, rx3, ry3

def show(image):
	cv2.namedWindow("output", cv2.WINDOW_NORMAL)
	cv2.imshow("output", image)
	cv2.waitKey()

if __name__ == "__main__":
	info = getInfo("ss1.png", "ss2.png", "ss3.png")
	print(info)



