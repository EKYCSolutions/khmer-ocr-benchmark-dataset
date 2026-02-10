
import json
import numpy as np
import cv2
import os 

def process(directory):
    for file in os.listdir(directory): 
    
        if os.path.splitext(file)[1] == ".json":

            json_file = open(os.path.join(directory, file))
            json_file = json.load(json_file)


            result_folder = os.path.join(directory + json_file["imagePath"][0:-5])
            
            if(os.path.exists(result_folder) == False):
                os.makedirs(result_folder)

            count = 1
           
            for shape in json_file['shapes']:
    
                img = cv2.imread(os.path.join(directory, json_file["imagePath"]))

                mask = np.zeros(img.shape[0:2], dtype=np.uint8)
                points = np.array([shape["points"]], dtype="int32")

                #method 1 smooth region
                cv2.drawContours(mask, [points], -1, (255, 255, 255), -1, cv2.LINE_AA)
                #method 2 not so smooth region
                # cv2.fillPoly(mask, points, (255))
                res = cv2.bitwise_and(img,img,mask = mask)
                rect = cv2.boundingRect(points) # returns (x,y,w,h) of the rect
                cropped = res[rect[1]: rect[1] + rect[3], rect[0]: rect[0] + rect[2]]
                ## crate the white background of the same size of original image
                wbg = np.ones_like(img, np.uint8)*255
                cv2.bitwise_not(wbg,wbg, mask=mask)
                # overlap the resulted cropped image on the white background
                # cv2.imshow("Mask",mask)
                cv2.imwrite(os.path.join(result_folder, f"{count}.png"), cropped)
                count+= 1
                

if __name__ == '__main__':
   json_dir = '/Users/menghang/Desktop/khob/TIFF/'
   process(json_dir)
   