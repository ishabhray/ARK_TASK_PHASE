import numpy as np
import random
import cv2

face_cascade = cv2.CascadeClassifier('/home/rishabh/OpenCV/data/haarcascades/haarcascade_frontalface_default.xml')

def check(x,y,c,obsx):

	if x<obsx[0][0]+25 or x>obsx[0][1]-25:
		return -1000
	return c

def play(img,k,obsx,c):
	x,y=250+k,100
	img=cv2.circle(img, (x,y),25, (255,255,0), -2)
	if c==500:
		for i in range(5):
			obsx[i]=create()
	if c==0:
		for i in range(4):
			obsx[i]=obsx[i+1]
		obsx[4]=create()
		c=150
	for i in range(5):
		cv2.rectangle(img,(0,c+150*i),(obsx[i][0],c+50+150*i),(0,150,250),-2)
		cv2.rectangle(img,(obsx[i][1],c+150*i),(500,c+50+150*i),(0,150,250),-2)
	if c<=125 and c>=25:
		c=check(x,y,c,obsx)
	cv2.imshow('game',img)
	cv2.waitKey(60)
	return img,c-5,obsx

def create():
	while True:
		x=50+random.random()*400
		y=50+random.random()*400
		if 500-(x+y) >=75:
			return np.int64(x),np.int64(500-y)

cap=cv2.VideoCapture(0)
#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1440)

while True:
	_,frame=cap.read()
	gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	if faces!=():
		break
for (x1,y1,w1,h1) in faces:
	xi,yi,w,h=x1,y1,w1,h1
track_window=(xi,yi,w,h)

roi=frame[yi:yi+h, xi:xi+w]
hsv_roi=cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
mask=cv2.inRange(hsv_roi, np.array((0.,60.,32.)),np.array((180.,255.,255.,)))
roi_hist=cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)

term_crit=(cv2.TERM_CRITERIA_EPS|cv2.TERM_CRITERIA_COUNT,10,1)
c=500
obsx=np.array([[0,0],[0,0],[0,0],[0,0],[0,0]])#obstacle array
while True:
	ret,frame=cap.read()
	if ret==True:
		hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
		dst=cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)
		ret,track_window=cv2.meanShift(dst,track_window,term_crit)
		x,y,w,h=track_window
		img2=cv2.rectangle(frame, (x,y), (x+w,y+h), 255,2)

		board=np.zeros((500,500,3), np.uint8)
		
		board,c,obsx=play(board,x-xi,obsx,c)

		cv2.imshow('img2', img2)

		k=cv2.waitKey(60) & 0xFF
		if k==27 or c==-1005:
			cv2.imwrite("GAMEOVER.jpg", board)
			break
	else:
		break
cv2.destroyAllWindows()
cap.release()
