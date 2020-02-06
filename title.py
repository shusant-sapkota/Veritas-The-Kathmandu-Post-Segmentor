import cv2
import numpy as np
import pytesseract
from pythonRLSA import rlsa
import math

def title(image_received):	

	image = image_received # reading the image



	#step 1: Image to Binary


	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #converting into greyscale

	(thresh,binary) = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU) #converting into binary image



	# Step 2: Contouring.

	#creating blank image same dimension as the given image.
	mask = np.ones(image.shape[:2], dtype="uint8")*255
	imghsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

	mask_blue = cv2.inRange(imghsv, (0,0,0), (20,20,20))

	(contours, _) = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) #finding contours i.e all letters

	#print(len(contours))

	#collecting all the heights of each contours
	heights = [cv2.boundingRect(contour)[3] for contour in contours]

	#finding average height
	average_height = sum(heights)/len(heights)

	#drawing contours

	for contour in contours:
		#drawing rectangles around the countours in main image

		[x,y,w,h] = cv2.boundingRect(contour)
		if (h > 2*average_height):
			#mask = cv2.rectangle(image, (x,y), (x+w, y+h), (0, 255, 0), 1)
			cv2.drawContours(mask, [contour], -1, 0, -1)


	'''
	cv2.namedWindow('filter',cv2.WINDOW_NORMAL)
	cv2.imshow('filter', mask)
	#cv2.imwrite('headlines.jpg',mask)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	'''
	
	


	#step 3: applying RLSA Horizontal on the image

	

	x,y = mask.shape

	value = max(math.ceil(x/100), math.ceil(y/100))+50
	mask = rlsa.rlsa(mask, True, False, value)

	'''
	cv2.namedWindow('rlsah',cv2.WINDOW_NORMAL)
	cv2.imshow('rlsah', mask)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	'''
	
	#step 4: applying above image in main image


	#finding contours
	(contours, _) = cv2.findContours(~mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	#blank image
	mask2 = np.ones(image.shape, dtype="uint8")*255

	for contour in contours:
		[x, y, w, h] = cv2.boundingRect(contour)
		if w > 0.60*image.shape[1]:
			title = image[y: y+h, x: x+w]

			mask2[y: y+h, x: x+w] = title #copied title contour onto the blank image
			image[y: y+h, x: x+w] = 255	#nullified the contour on original image


	'''
	cv2.namedWindow('title',cv2.WINDOW_NORMAL)
	cv2.imshow('title', mask2)
	#cv2.imwrite('headlines.jpg',mask)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	'''

	extracted_title = pytesseract.image_to_string(mask2)
	return(extracted_title)

	