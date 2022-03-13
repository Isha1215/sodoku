print('SETTING_UP')
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='3'  ## to avoid warning messages from tensorflow
from utilities import *
import sudoku_solver
import cv2
import numpy as np
path="Resources/sudoko3.jpg"
img_height=450
img_width=450
img=cv2.imread(path)
img=cv2.resize(img,(img_width,img_height)) #order(w,h) resize to make it a square
img_blank=np.zeros((img_height,img_width,3),np.uint8)
imgThreshold= preprocess(img)


img_contours=img.copy()
img_big_contour=img.copy()
contours,heirarchy=cv2.findContours(imgThreshold,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
cv2.drawContours(img_contours,contours,-1,(0,255,0),3)

biggest,max_area=biggest_contour(contours)

if biggest.size!=0:
    biggest=preorder(biggest)
    cv2.drawContours(img_big_contour,biggest, -1, (0, 0, 255), 25)
    pts1=np.float32(biggest)
    pts2=np.float32([[0,0],[img_width,0],[0,img_height],[img_width,img_height]])
    matrix=cv2.getPerspectiveTransform(pts1,pts2)
    img_wrap_colored=cv2.warpPerspective(img,matrix,(img_width,img_height))
    img_detect_digits=img_blank.copy()
    img_wrap_colored=cv2.cvtColor(img_wrap_colored,cv2.COLOR_BGR2GRAY)

boxes=splitboxes(img_wrap_colored)
model=initializeModel()
images=prediction(boxes,model)
print(images)
img_detect_digits=display(img_detect_digits,images,color=(255,0,0))
images=np.asarray(images)
posArray=np.where(images>0,0,1)
board=np.array_split(images,9)
try:
    sudoku_solver.solve(board)
except:
    pass

flat_list=[]
for i in board:
    for j in i:
        flat_list.append(j)
image_solved_digits=img_blank.copy()
flat_list=flat_list*posArray
image_solved_digits=display(image_solved_digits,flat_list,color=(0,0,255))
p1=np.float32(biggest)
p2=np.float32([[0,0],[img_width,0],[0,img_height],[img_width,img_height]])
mat=cv2.getPerspectiveTransform(p2,p1)
img_inv_perspective=cv2.warpPerspective(image_solved_digits,mat,(img_width,img_height))
img_overlay=cv2.addWeighted(img_inv_perspective,1,img,0.5,1)
image_solved_digits=grid(image_solved_digits)
img_detect_digits=grid(img_detect_digits)
final=StackedImages(0.6,([img_overlay,imgThreshold,img_contours,img_big_contour],[img_wrap_colored,img_detect_digits,image_solved_digits,img_inv_perspective]))
cv2.imshow('final',final)
cv2.waitKey(0)
