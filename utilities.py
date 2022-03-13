import cv2
import numpy as np
from tensorflow.keras.models import load_model

def initializeModel():
    model=load_model("C:/Users/ishad/Documents/prog/PycharmProjects/sodoku/model_trained.h5")
    return model
def preprocess(img):
    img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img_blurr=cv2.GaussianBlur(img_gray,(5,5),0)
    img_threshold=cv2.adaptiveThreshold(img_blurr,255,1,1,13,3)
    return img_threshold
def preprocessing(img):
    img=cv2.equalizeHist(img) #used to equally distribute intensities throughout the picture
    img=img/255 # we want the image range between (0-1) applying normalization
    return img
def StackedImages(scale,imgArray):
    rows=len(imgArray)
    cols=len(imgArray[0])
    rows_available=isinstance(imgArray[0],list)
    width=imgArray[0][0].shape[1]
    height=imgArray[0][0].shape[0]
    if rows_available:
        for x in range(0,rows):
            for y in range(0,cols):
                if imgArray[x][y].shape[:2]==imgArray[0][0].shape[:2]:
                    imgArray[x][y]=cv2.resize(imgArray[x][y],(0,0),None,scale,scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1],imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape)==2:
                    imgArray[x][y]=cv2.cvtColor(imgArray[x][y],cv2.COLOR_GRAY2BGR)

        black_img=np.zeros((height,width,3),np.uint8)
        hor=[black_img]*rows
        hor_con=[black_img]*rows
        for x in range(0,rows):
            hor[x]=np.hstack(imgArray[x])
        ver=np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2:
                imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor

    return ver



def biggest_contour(contours):
    biggest=np.array([])
    max_area=0
    for cnt in contours:
        area=cv2.contourArea(cnt)
        if area>50:
            peri=cv2.arcLength(cnt,True)
            approx=cv2.approxPolyDP(cnt,0.02*peri,True)
            if area>max_area and len(approx)==4:
                biggest=approx
                max_area=area
    return biggest,max_area

def preorder(biggest):
    points=biggest.reshape(4,2)
    new_points=np.zeros((4,1,2),dtype=np.int32)
    add=points.sum(1)
    diff=np.diff(points)
    new_points[0]=points[np.argmin(add)]
    new_points[3]=points[np.argmax(add)]
    new_points[1]=points[np.argmin(diff)]
    new_points[2]=points[np.argmax(diff)]
    return new_points

def splitboxes(img):
    boxes=[]
    rows=np.vsplit(img,9)    #splits row wise
    for r in rows:
        cols=np.hsplit(r,9)   #splits column wise
        for c in cols:
            boxes.append(c)
    return boxes

def prediction(boxes,model):
    images=[]
    for i in boxes:
        img=np.asarray(i)
        img=img[5:img.shape[0]-5,5:img.shape[1]-5]
        img=cv2.resize(img,(32,32))
        img=img/255
        img=img.reshape(1,32,32,1)
        predictions=model.predict(img)
        classIndex=np.argmax(predictions,axis=-1)
        probVal=np.amax(predictions)
        #print(classIndex,probVal)
        if probVal>0.55:
            images.append(classIndex[0])
        else:
            images.append(0)
    return images


def display(img,images,color):
    h=int(img.shape[0]/9)
    w = int(img.shape[1] / 9)
    for x in range(0,9):
        for y in range(0,9):
            if images[(x*9)+y]!=0:
                cv2.putText(img,str(images[(x*9)+y]),(y*w+int(w/2)-10,int((x+0.8)*h)),cv2.FONT_HERSHEY_COMPLEX,1,color,2,cv2.LINE_AA)

    return img

def grid(img):
    h=int(img.shape[0]/9)
    w=int(img.shape[1]/9)
    for i in range(0,9):
        p1=(0,h*i)
        p2=(img.shape[1],h*i)
        p4=(w*i,img.shape[0])
        p3=(w*i,0)
        cv2.line(img,p1,p2,(0,255,0),2)
        cv2.line(img, p3, p4, (0, 255, 0), 2)
    return img