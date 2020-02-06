import sys
import cv2
import numpy as np
import pytesseract
import tts
import title


'''
The segmentation process is completed in three process:
'''
def segmenter(image_received):

  # Process 1: Lines Detection

  img = image_received
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  #convert to binary gray image
  edges = cv2.Canny(gray, 75, 150)			# determine contours
  lines = cv2.HoughLinesP(edges, 0.017, np.pi/180,60,minLineLength=100, maxLineGap=0.1) #houghlines generation


  #drawing houghlines
  for line in lines:
    x1, y1, x2, y2 = line[0]
    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 128), 12)  #the houghlines of color (0,0,128) is drawn


  #Drawing brown border
  bold = cv2.copyMakeBorder(
                  img,	#image source
                  10, 	#top width
                  10, 	#bottomm width
                  10, 	#left width
                  10, 	#right width
                  cv2.BORDER_CONSTANT, 
                  value= (0,0,128) #brown color value
                )


  '''
  #The lines are bolded and the final image is displayed:
  
  
  cv2.namedWindow("LinesDetectedt",cv2.WINDOW_NORMAL)
  cv2.imshow("LinesDetected", bold)
  #cv2.imwrite('a.jpg',bold)

  cv2.waitKey(0)
  cv2.destroyAllWindows()
  '''




  image = bold
  gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
  thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]


  horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10,1))
  detected_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
  cnts = cv2.findContours(detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
  cnts = cnts[0] if len(cnts) == 2 else cnts[1]
  for c in cnts:
    if int(len(c) >= 1000):
      cv2.drawContours(image, [c], 0, (0,17,255), 25)


  
  vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,10))
  detected_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
  cnts = cv2.findContours(detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
  cnts = cnts[0] if len(cnts) == 2 else cnts[1]
  for c in cnts:
    if int(len(c) >= 1000):
      cv2.drawContours(image, [c], 0, (0,17,255), 25)


  cv2.namedWindow("image",cv2.WINDOW_NORMAL)
  cv2.imshow('image', image)
  cv2.waitKey(0)
  cv2.destroyAllWindows()



  # Process 3: Contour Detection and Segmentaion.


  img = image  #image with lines are assigned as img
  imghsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)



  mask_blue = cv2.inRange(imghsv, (0,20,20), (8,255,255))
  contours, _ = cv2.findContours(mask_blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

  noc = int(len(contours))



  print('Numbers of contours found=' + str(len(contours)))
  article_no = 1
  count = 1
  #largestContourArea = 0
  #largestContour = 0
  for cnt in contours:
      contourArea = cv2.contourArea(cnt)
      if (contourArea > 18432):
        x,y,w,h = cv2.boundingRect(cnt)
        ROI = img[y:y+h,x:x+w]
        '''
        when count == 1, whole newspaper page is identified as a single countour
        In order to ease the extraction process this whole page is neglected
        ''' 
        if (count !=1):
          extracted_text = pytesseract.image_to_string(ROI) # in this step the article text is extracted from segment
          #name = "segment_%d.jpg" %(count-1) #this step is saving each segment successively

          #the extr
          if(len(extracted_text) > 2000):
            #There is complete article in this segment with headline
            cv2.namedWindow("News Segment",cv2.WINDOW_NORMAL)
            cv2.imshow("News Segment",ROI)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


            article_title = title.title(ROI)
            print("Article no. %d: \n %s"%((article_no),(article_title)))
            condition = input("Full Article ? :->   y - YES, anyother - NO : ")

            if (condition=='y'):
              '''
              # There is no headline in this segment
              print(extracted_text)
              cv2.namedWindow("News Segment",cv2.WINDOW_NORMAL)
              cv2.imshow("News Segment",ROI)
              cv2.waitKey(0)
              cv2.destroyAllWindows()
              print('##############################################################')
              '''
              print(extracted_text)
              print('##############################################################')

              condition = input("Audio ? :->   y - YES, anyother - NO : ")
              if (condition=='y'):
                tts.tts(extracted_text)
                                    
            '''
            #for saving each segment successively
            name = "segment_%d.jpg" %(save)
            cv2.imwrite(name,ROI)
            
            '''
            
            article_no = article_no+1
          
        
      count = count+1
    




