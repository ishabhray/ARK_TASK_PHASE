import cv2
import numpy as np
import math

def dist(x1,y1,x2,y2):
	return math.sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1)) 

def coll_bnb(circles,cir):
	c=0
	for circle in circles[0, :]:
		if np.array_equal(circle,cir) : #skipping if checking collision between 2 arrays
			c+=1
			continue;
		d=dist(circle[0],circle[1],cir[0],cir[1])-circle[2]-cir[2]
		if d<1.0 :
			return c
		c+=1
	return -1

#returns which wall the ball strikes
def coll_bnw(circle,rows,cols):
	if circle[0]<=circle[2] :
		circle[0]=circle[2]#prevent ball from going inside the table
		return 'L'
	elif circle[0]>=cols-circle[2] :
		circle[0]=cols-circle[2]
		return 'R'
	elif circle[1]<=circle[2] :
		circle[1]=circle[2]
		return 'U'
	elif circle[1]>=rows-circle[2] :
		circle[1]=rows-circle[2]
		return 'D'

def print_circle(new,circles):
	for cir in circles[0, :]:
		cv2.circle(new,(cir[0],cir[1]),cir[2],(0,0,255),-2)
	cv2.imshow('img',new)
	return(cv2.waitKey(5))

def optimize_delx_dely(delx,dely):
	if delx==0:
		dely/=abs(dely)
	elif dely==0:
		delx/=abs(delx)
	elif abs(dely)>=abs(delx):
		dely/=abs(delx)
		delx/=abs(delx)
		if(abs(dely)>15):
			dely/=abs(dely)
			delx=0;
	else:
		delx/=abs(dely)
		dely/=abs(dely)
		if(abs(delx)>15):
			delx/=abs(delx)
			dely=0;
	return int(delx),int(dely)

img = cv2.imread('1.png',1)
rows,cols,_=img.shape
gray  = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
gblur = cv2.medianBlur(gray,5)
edges = cv2.Canny(gray,50,150,apertureSize = 3)

circles = cv2.HoughCircles(gblur,cv2.HOUGH_GRADIENT,1,10,param1=50,param2=10,minRadius=20,maxRadius=30)
circles = np.int64(np.around(circles)) #coverts all float values to decimals

lines = cv2.HoughLinesP(edges,1,np.pi/180,10,100,50)
lines = np.int64(np.around(lines))

#finding the line representing the cue
cue=lines[0,0]
length=1000
for i in range(0,len(lines)):
    for x1,y1,x2,y2 in lines[i]:
    	d=dist(x1,y1,x2,y2)
    	if(d<length):
    		length=d
    		cue=x1,y1,x2,y2


#finding direction of cue hit
dely=(cue[3]-cue[1])*1.0
delx=(cue[2]-cue[0])*1.0

#finding ball hit by cue
ball_hit=circles[0,0]
dis=dist(ball_hit[0],ball_hit[1],cue[2],cue[3])
for cir in circles[0, :]:
	d=dist(cir[0],cir[1],cue[2],cue[3])
	if(d<dis):
		dis=d
		ball_hit=cir

cv2.imshow('img',img)
cv2.waitKey(0)

while True:
	delx,dely=optimize_delx_dely(delx,dely)
	ball_hit[0]+=delx
	ball_hit[1]+=dely
	new=np.zeros((rows,cols,3), np.uint8)
	k=print_circle(new,circles)
	if k== ord('q'):
		break;
	ch=coll_bnw(ball_hit,rows,cols)
	if(ch=='L' or ch=='R'):
		delx=-delx
		continue
	if(ch=='U' or ch=='D'):
		dely=-dely
		continue
	ch=coll_bnb(circles,ball_hit)
	if ch!=-1:
		cir=circles[0,ch]
		dely=(cir[1]-ball_hit[1])*1.0
		delx=(cir[0]-ball_hit[0])*1.0
		delx,dely=optimize_delx_dely(delx,dely)
		ball_hit=cir
		ball_hit[0]+=delx
		ball_hit[1]+=dely
cv2.destroyAllWindows()
