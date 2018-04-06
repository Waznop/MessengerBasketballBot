from uiautomator import device as d
from imageproc import getInfo
import time

file1 = "ss1.png"
file2 = "ss2.png"
file3 = "ss3.png"
swipeSpeed = 12
projActDelay = 1.2
changeDirThreshold = 1.2
turnDelay = 1.5
minX, maxX = 100, 980
minY, maxY = 100, 1820

def play():
	try:
		turn = 1
		while True:
			print("Turn {}".format(turn))
			swipe()
			turn += 1
			time.sleep(turnDelay)
	except KeyboardInterrupt:
		pass

def swipe():
	d.screenshot(file1)

	t = time.time()

	d.screenshot(file2)

	screen1Delay = time.time() - t
	t = time.time()

	d.screenshot(file3)

	screen2Delay = time.time() - t
	t = time.time()

	bx, by, rx1, ry1, rx2, ry2, rx3, ry3 = getInfo(file1, file2, file3)
	vx1 = (rx2 - rx1) / screen1Delay
	vy1 = (ry2 - ry1) / screen1Delay
	vx2 = (rx3 - rx2) / screen2Delay
	vy2 = (ry3 - ry2) / screen2Delay

	# account for direction changing
	changedDir = vx2 != 0 and abs(vx1) / abs(vx2) > changeDirThreshold
	if changedDir:
		projrx3 = rx2 + vx1 * screen2Delay
		changedDir = projrx3 < minX or projrx3 > maxX
	if changedDir:
		print("Changed direction: vx1: {:f}, vx2: {:f}, vy1: {:f}, vy2: {:f}".format(vx1, vx2, vy1, vy2))
	vx = -vx1 if changedDir else vx2
	vy = -vy1 if changedDir else vy2

	procDelay = time.time() - t
	t = time.time()

	rx = rx3 + vx * (procDelay + projActDelay)
	ry = ry3 + vy * (procDelay + projActDelay)

	# account for screen limits
	usedT = 0
	if rx > maxX:
		usedT = (maxX - rx3) / vx
		rx = maxX - vx * (procDelay + projActDelay - usedT)
	elif rx < minX:
		usedT = (minX - rx3) / vx
		rx = minX - vx * (procDelay + projActDelay - usedT)
	if ry > maxY:
		usedT = (maxY - ry3) / vy
		ry = maxY - vy * (procDelay + projActDelay - usedT)
	elif ry < minY:
		usedT = (minY - ry3) / vy
		ry = minY - vy * (procDelay + projActDelay - usedT)
	if usedT != 0:
		print("Out of bounds: usedT: {:f}, rx: {:f}, ry: {:f}".format(usedT, rx, ry))

	d.swipe(bx, by, rx, ry, swipeSpeed)

	actDelay = time.time() - t

	if vx != 0:
		print("Ball: ({}, {})\nRing: ({}, {}) -> ({}, {}) -> ({}, {})\nTarget: ({}, {})".format(bx, by, rx1, ry1, rx2, ry2, rx3, ry3, rx, ry))
		print("Delays: ({:f}, {:f}, {:f}, {:f})".format(screen1Delay, screen2Delay, procDelay, actDelay))

if __name__ == "__main__":
	play()

