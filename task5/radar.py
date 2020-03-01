from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import style
from scipy.optimize import curve_fit
import pandas as pd
import numpy as np

def para(t,pol):
	for i in range(0,t.shape[0]):
		t[i]=t[i]**2*pol[0]+t[i]*pol[1]+pol[2]
	return t

style.use('ggplot')
df=pd.read_csv("radar_dump.csv")

fig=plt.figure()
ax1=fig.add_subplot(111,projection='3d')
ax1.set_xlabel('x-axis')
ax1.set_ylabel('y-axis')
ax1.set_zlabel('z-axis')

x=df.iloc[150:300,0]
y=df.iloc[150:300,1]
z=df.iloc[150:300,2]

t=np.arange(x.shape[0],dtype=np.float)
fitx = np.polyfit(t, x, 2)
fity = np.polyfit(t, y, 2)
fitz = np.polyfit(t, z, 2)

xf=para(t,fitx)
t=np.arange(x.shape[0],dtype=np.float)
yf=para(t,fity)
t=np.arange(x.shape[0],dtype=np.float)
zf=para(t,fitz)


ax1.scatter(x,y,z,marker='.')
ax1.scatter(xf,yf,zf,c='b',marker='.')
plt.show()