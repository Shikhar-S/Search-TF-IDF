import matplotlib.pyplot as plt 
import os,sys
from scipy.optimize import curve_fit

def func(x,a,b,c,d):
	return a*x*x*x + b*x*x + c*x +d 

cwd=os.getcwd()
folder=raw_input('Folder name:\n')
pth=os.path.join(cwd,folder)
x_final=list()
y_final=list()
count=0
for filename in os.listdir(pth):
	if(filename!='.DS_Store'):
		count+=1
		x=list()
		y=list()
		print filename
		
		with open(os.path.join(pth,filename),'r') as F:
			for line in F:
				line=line.split()
				y.append(float(line[0]))
				x.append(float(line[1]))		
				
		params=curve_fit(func,x,y)
		[a,b,c,d]=params[0]
		i=0
		x_new=list()
		y_new=list()
		j=0
		while i<=1.0:
			x_new.append(i)
			temp=func(i,a,b,c,d)
			y_new.append(temp)
			
			if count==1:
				x_final.append(i)
				y_final.append(temp)
			else:
				x_final[j]+=i
				y_final[j]+=temp
			j+=1
			i+=0.1

for j in xrange(0,10):
	x_final[j]/=count
	y_final[j]/=count	
plt.plot(x_final,y_final)
plt.axis([0.0,1.0,0.0,1.0])
plt.show()
		