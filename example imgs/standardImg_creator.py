'''
makes a standard image for pattern matching to match against new array images.
saves the positional information for the spots and the radii as a .json file for future use
the position/radii information is stored as a json for easy retrieval
as dict objects.



'''

# import libraries 
import numpy as np 
import cv2
import json
import base64
#from pymongo import MongoClient

# PARAMETERS SET UP

automatic = True
numSpots = 5









arrayCoords = []
def mouseLocationClick(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("click identified at: " +str([x,y]))
        arrayCoords.append([x,y])

def cvWindow(nameOfWindow, imageToShow, keypressBool):
    print("----------Displaying: "
          + str(nameOfWindow)
          + "    ----------")
    cv2.namedWindow(nameOfWindow, cv2.WINDOW_NORMAL)
    cv2.setMouseCallback(nameOfWindow, mouseLocationClick)
    cv2.imshow(nameOfWindow, imageToShow)
    pressedKey = cv2.waitKey(0)
    cv2.destroyAllWindows()
    if keypressBool:
        return pressedKey

def circlePixelID(circleList): # output pixel locations of all circles within the list,
    circleIDpointer = 0
    pixelLocations = []
    for eachCircle in circleList:
#        print("this circle is being analyzed in circle pixel ID")
#        print(eachCircle)
        xCoordCirc = eachCircle[0] # separates the x and y coordinates of the center of the circles and the circle radius 
        yCoordCirc = eachCircle[1]
        radiusCirc = eachCircle[2]
        for exesInCircle in range(( xCoordCirc - radiusCirc ),( xCoordCirc + radiusCirc )):
            whyRange = np.sqrt(pow(radiusCirc,2) - pow((exesInCircle - xCoordCirc),2)) #calculates the y-coordinates that define the top and bottom bounds of a slice (at x position) of the circle 
            discreteWhyRange = int(whyRange) 
            for whysInCircle in range(( yCoordCirc - discreteWhyRange),( yCoordCirc + discreteWhyRange)):
                pixelLocations.append([exesInCircle,whysInCircle, radiusCirc, circleIDpointer])
        circleIDpointer = circleIDpointer + 1 
    return pixelLocations


def encodeImage(np_img_array):
    _, img_buffer = cv2.imencode(".tiff", np_img_array)
    img_buffer_enc64 = base64.b64encode(img_buffer)
    str_img_buffer_enc64 = str(img_buffer_enc64, encoding='utf-8')
    return str_img_buffer_enc64


#fileName = input("give file name within this directory for std generation: ")
#imgRaw = cv2.imread(fileName, 0)
imgRaw = cv2.imread("slide1_2.tiff", 0) # import the raw image

print("click positions (2) top left and bottom right corner bounds for the std. press d when done")
keyPress= cvWindow('Raw Image',imgRaw, True)
if keyPress == ord('d'):
    arrayBotRigCoords = arrayCoords.pop()
    arrayTopLefCoords = arrayCoords.pop()
    print("subplot coordinates: " + str(arrayBotRigCoords)+ " " + str(arrayTopLefCoords))

cropXCoords = sorted([arrayBotRigCoords[0],arrayTopLefCoords[0]])
cropYCoords = sorted([arrayBotRigCoords[1],arrayTopLefCoords[1]])
print(str(cropXCoords))
print(str(cropYCoords))
subImg = imgRaw[cropYCoords[0]:cropYCoords[1],cropXCoords[0]:cropXCoords[1]].copy()

if automatic:
    smoothedIMG = cv2.medianBlur(subImg,3)
    circlesD = cv2.HoughCircles(smoothedIMG,
                                cv2.HOUGH_GRADIENT,1,
                                minDist = 80,
                                param1 = 15,
                                param2 = 21,
                                minRadius = 28,
                                maxRadius = 32)
    circlesX = np.uint(np.around(circlesD))
    circleLocs = circlesX[0]
    
    verImg = cv2.cvtColor(subImg.copy(), cv2.COLOR_GRAY2RGB)
    
    idealStdImg = np.zeros(subImg.shape, dtype=np.uint8)
    circlePixels = circlePixelID(circleLocs)
    for eachPixel in circlePixels:
        idealStdImg[eachPixel[1], eachPixel[0]] = 100
        
    for eachCircle in circleLocs:
        cv2.circle(verImg,
                   (eachCircle[0], eachCircle[1]),
                   eachCircle[2]+4,
                   (30,30,255),
                   3)
        cv2.circle(verImg,
                   (eachCircle[0], eachCircle[1]),
                   2,
                   (30,30,255),
                   2)
        cv2.circle(idealStdImg,
                   (eachCircle[0], eachCircle[1]),
                   eachCircle[2],
                   255,
                   3)
               
    cvWindow("verif image", verImg, False)
    cvWindow("pattern generated", idealStdImg, False)
                   
else:
    print("click centers of circles, then click (2) points that establish a horiz diameter of one circle. press x when done")
    keyPress= cvWindow('Cropped Image', subImg, True)

    diam1 = arrayCoords.pop()
    diam2 = arrayCoords.pop()
    fullDiam = abs(diam1[0]-diam2[0])
    circleLocs = []
    for each in range(numSpots):
        coords = arrayCoords.pop()
        circleLocs.append([coords[0],
                           coords[1],
                           round(fullDiam/2)])

    # Generates the ideal std image from the cropped array image
    idealStdImg = np.zeros(subImg.shape, dtype=np.uint8)
    circlePixels = circlePixelID(circleLocs)
    for eachPixel in circlePixels:
        idealStdImg[eachPixel[1], eachPixel[0]] = 50
    cvWindow("testIdeal", idealStdImg, False)

imageOutName = "standard_leptin_1-coffee-ring.tiff"
cv2.imwrite(imageOutName, idealStdImg)
encoded_stdImg = encodeImage(idealStdImg)

stdSpotDict = {"batch" : "leptin-1",
               "spot_info": circleLocs.tolist(),
               #"image": encoded_stdImg,
               "shape": [idealStdImg.shape[0],idealStdImg.shape[1]]}

#client = MongoClient()
#db = client.test_database
#db.patterns.insert_one(stdSpotDict)

jsonFileOutName = "standard_leptin_1-coffee-ring.json"
out_file = open(jsonFileOutName, "w")
json.dump(stdSpotDict, out_file)
out_file.close()

















