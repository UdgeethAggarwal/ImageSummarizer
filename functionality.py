import cv2 
import numpy as np 
import sys
import random
import pytesseract
import os
import string
import time
def detect_lines(img):
	gray=cv2.cvtColor(img.copy(),cv2.COLOR_BGR2GRAY)
	img_sobel = cv2.Sobel(gray, cv2.CV_8U, 1, 0, ksize=1, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
	ret2,img_threshold = cv2.threshold(img_sobel,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	blank_image = np.zeros((img.shape[0],img.shape[1],3), np.uint8)
	ln,wd=1,1
	kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(int(17*ln),int(3*wd)))
	img_threshold = cv2.morphologyEx(img_threshold, cv2.MORPH_CLOSE, kernel)
	contours, hierarchy = cv2.findContours(img_threshold,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	contours_poly = []
	contour_size=100
	actCont=[]
	for c in contours:
		rand = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(10)])
		if len(c) < contour_size:
		    continue
		poly = cv2.approxPolyDP(c, epsilon=3, closed=True)
		x, y, w, h = cv2.boundingRect(poly)
		if w > 2*h:
			rect = cv2.minAreaRect(c)
			box = cv2.boxPoints(rect)
			box = np.int0(box)
			actCont.append(c)
			contours_poly.append([x, y, w, h])
			# cv2.drawContours(img,c,-1,(0,0,255),3)
			# cv2.drawContours(blank_image,[box],-1,(0,0,255),3)
			part=img_threshold[y:y+h,x:x+w].copy()
			cont,_=cv2.findContours(part.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
			c1 = max(cont, key = cv2.contourArea)

			blank_image = np.zeros((h,w,3), np.uint8)
			white_image = 255*np.ones((h,w,3), np.uint8)

			# cv2.drawContours(blank_image,c1,-1,(255,255,255),3)
			kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(int(17),int(11)))

			blank_image = cv2.morphologyEx(blank_image, cv2.MORPH_CLOSE, kernel,10)

			kernel = np.ones((10,1),np.uint8)
			blank_image = cv2.dilate(blank_image,kernel,iterations = 1)
			# # blank_image=cv2.cvtColor(blank_image,cv2.COLOR_BGR2GRAY)
			# print (part.shape,blank_image.shape)
			# final=cv2.bitwise_and(img[y:y+h,x:x+w], blank_image)
			# final=cv2.bitwise_and(final, white_image)


			# pytesseract.pytesseract.tesseract_cmd = r"D:\\bin\\tesseract.exe" #path where tesseract is installed
			# # (?# pytesseract.pytesseract.tesseract_cmd = r"D:\\tesseract5\\tesseract.exe" #path where tesseract is installed)--tessdata-dir D:\\tesseract5\\tessdata 

			# txt=pytesseract.image_to_string(final,lang='eng_fast',config='--psm 6')
			# print (txt)



			# cv2.namedWindow("imgo",cv2.WINDOW_KEEPRATIO)
			# cv2.imshow("imgo",final)

			# cv2.namedWindow("imgt",cv2.WINDOW_KEEPRATIO)
			# cv2.imshow("imgt",blank_image)
			# cv2.namedWindow("imgt2",cv2.WINDOW_KEEPRATIO)
			# cv2.imshow("imgt2",part)
			# # cv2.imshow("imgo",img[y:y+h,x:x+w])

			# cv2.waitKey(0)
			# cv2.destroyAllWindows()
	# 		cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
	# cv2.namedWindow("frame",cv2.WINDOW_NORMAL)
	# cv2.imshow("frame",img)
	# cv2.namedWindow("frame1",cv2.WINDOW_NORMAL)
	# cv2.imshow("frame1",img_threshold)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()
	return contours_poly,actCont,img_threshold
def doPara(imageName):
	img = cv2.imread(imageName, cv2.IMREAD_COLOR)
	img1=img.copy()
	img=cv2.resize(img,(960,1280))
	imageFinal=img.copy()
	res,contours,img_threshold = detect_lines(img)
	if len(res)==0:
		return(False)
	med=np.median(np.array(res),axis=0)
	res.sort(key=lambda r:(r[1]))
	cont=0
	for i in range(len(res)-1):
		res[i].append(cont)
		xc,yc,wc,hc,_=res[i]
		xn,yn,wn,hn=res[i+1]
		if yn-yc>med[3]/2.0:
			cont+=1
	res[-1].append(cont)
	res.sort(key=lambda r:(r[4],r[0]))
	blank_image = np.zeros((img.shape[0],img.shape[1],3), np.uint8)
	text=""
	prevLine=-1
	i=0
	count=0
	for r in res:
		x,y,w,h,line=r
		x=x-10
		y=y-10
		w=w+20
		h=h+20
		fnl=imageFinal[y:y+h,x:x+w]
		fnlThresh=img_threshold[y:y+h,x:x+w]

		cmg=img_threshold[y-10:y+h+20,x-10:x+w+20].copy()
		#pth1="D:\\byju's\\test"
		i+=1
		contours, hierarchy = cv2.findContours(fnlThresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		if len(contours)>0:
			maxArea=0
			for cont in contours:
				area=cv2.contourArea(cont)
				if area>maxArea:
					cnt=cont
					maxArea=area
			# print (contours)
			poly = cv2.approxPolyDP(cnt, epsilon=3, closed=True)
			x1, y1, w1, h1 = cv2.boundingRect(poly)
			x1-=10
			y1-=10
			w1+=20
			h1+=20
			
			rect = cv2.minAreaRect(cnt)
			box1 = cv2.boxPoints(rect) # cv2.boxPoints(rect) for OpenCV 3.x
			box1 = np.int0(box1)
			rect=list(rect)
			rect[0]=list(rect[0])
			rect[1]=list(rect[1])

			rect[0][0]=rect[0][0]-2
			rect[0][1]=rect[0][1]-2
			rect[1][0]=rect[1][0]+4
			rect[1][1]=rect[1][1]+4
			rect[1][0]=round(rect[1][0])
			rect[1][1]=round(rect[1][1])

			rect[0]=tuple(rect[0])
			rect[1]=tuple(rect[1])

			rect=tuple(rect)
			center=rect[0]
			angle=rect[2]
			size=rect[1]
			if angle<-45:
				angle+=90
				var=list(size)
				temp=var[1]
				var[1]=var[0]
				var[0]=temp
				size=tuple(var)
			M = cv2.getRotationMatrix2D(center, angle, 1.0)
			rotated = cv2.warpAffine(fnl, M, (fnl.shape[1],fnl.shape[0]), flags=cv2.INTER_CUBIC)
			cropped=cv2.getRectSubPix(rotated, size, center)
			# cv2.namedWindow("crop",cv2.WINDOW_KEEPRATIO)
			# cv2.imshow("crop",cropped)
			# txt=''
			#pytesseract.pytesseract.tesseract_cmd = r"/Users/aparajitgarg/Desktop/bin/tesseract.exe" #path where tesseract is installed
			# (?# pytesseract.pytesseract.tesseract_cmd = r"D:\\tesseract5\\tesseract.exe" #path where tesseract is installed)--tessdata-dir D:\\tesseract5\\tessdata 

			txt=pytesseract.image_to_string(cropped,lang='eng_fast',config='--psm 6 --oem 1')
			# print (txt)
			# cv2.waitKey(0)
			# cv2.destroyAllWindows()
			if line==0 and count==0:
				text+=txt
				count=1


			elif line==prevLine:
				text+=" "+txt
			else:
				text+='\n'+txt
			prevLine=line
	cv2.destroyAllWindows()
	return(text)
folder=sys.argv[1]
#imageNames=os.listdir(folder)
# pth=os.path.join(os.getcwd(),"output_best")
pth=folder
print (pth)
if not os.path.exists(pth):
	os.makedirs(pth)
#for imageName in imageNames:
s1=time.time()
txt=doPara(folder)
e1=time.time()
print ("Time taken for image = ",folder),
print (" is => ",e1-s1)
#name,_=os.path.splitext(imageName)
#name+=".txt"
filename='created.txt'#os.path.join(pth,name)
if isinstance(txt, bool):
	txt=''
print (txt)
with open(filename,"w+") as f:
	f.write(txt)
		# f.write(str(txt.encode("utf-8")))