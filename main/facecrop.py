#author: Tomo Lapautre

import cv2
import numpy as np

import pathlib
from pathlib import Path
import glob
import os
from PIL import Image, ImageOps

from main.constants import (
    PNGS,
    CV2_FILETYPES,
    DNN_THRESHOLD,
    FAILED_IMAGE_FOLDER)       



class FaceCrop():
    
    def __init__(self, height, width, height_asy, width_asy, tag='A', pyqt_ui=None):
        
        self.width = width #The width of the cropped image, expressed as a percentage of the initial image width. (Int between 0 and 100)
        self.width_asy = width_asy #The horizontal assymmetry of the cropping area relative to the position of the face. 
        #Positive values will shift the image to the left of the face and negative values to the right (Integers)
        self.height = height #The height of the cropped image, expressed as a percentage of the initial image height. (Int between 0 and 100)
        self.height_asy = height_asy #The vertical assymmetry of the cropped area relative to the position of the face. 
        #Positive values will shift the image down from the face and negative values will shift the image up (Integers).
        self.tag = tag #The program will save the cropped image with its original file name + the file tag. Ex: IMG001 is saved as IMG001_A for a file tag of 'A'. Optional.
        self.failure_folder = FAILED_IMAGE_FOLDER #folder where images where faces couldn't be detected will be stored
        self.threshold = DNN_THRESHOLD #threshold of confidence to categorise as a face
        self.progress_count = 0 #to keep track of progress bar
        self.pyqt_ui = pyqt_ui #this variable is to integrate this class to your pyqt GUI so that, for example you can generate a progress bar

        #files of the trained neural network given by cv2
        self.modelFile = "main/res10_300x300_ssd_iter_140000.caffemodel"
        self.configFile = "main/deploy.prototxt.txt"
        self.net = cv2.dnn.readNetFromCaffe(self.configFile, self.modelFile)


    #finds the face and saves the cropped face in your output directory
    def crop_save(self, input_directory, output_path, bool_folder=False, bool_face_count=False, preview=False):
        #if 'bool_face_count' is set to True, program will only save one face per image (the one with the highest confidence)
        #if 'bool_folder' is set to True, program will save the new image in its seperate folder. This can be useful if you have multiple faces per image.
        #if 'preview' is set to True, only crops the first face it can find and returns the image.

        folder_name = pathlib.PurePath(input_directory).name
        files = glob.glob('{}/*'.format(input_directory)) #finds all the files in your directory

        if self.tag:
            self.tag = "_" + self.tag 
        
        #loops through all the files in the directory
        for i, file in enumerate(files):
            
            #updates the pyqt progress bar
            if not preview and self.pyqt_ui is not None:
                self.progress_count += 1
                self.pyqt_ui.progress.setValue(self.progress_count)
                
                #breaks program if user clicks on cancel button of progress bar
                if self.pyqt_ui.progress.wasCanceled():
                    break
    
            
            file_path = Path(file)
            file_name = file_path.stem
            ext = file_path.suffix

            #checks if image is readable by cv2
            if ext.lower() not in CV2_FILETYPES:
                continue
            
            image = cv2.imdecode(np.fromfile(file, dtype=np.uint8), cv2.IMREAD_COLOR)
        
            try:
                img_height, img_width = image.shape[:2]
            except AttributeError:
                print('{}: ImageReadError'.format(file_name))
                continue
    
            blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 117.0, 123.0)) #resize image
            self.net.setInput(blob)
            faces = self.net.forward()
            
            #reload image using PIL as cv2 isn't adapted in this scenario to read PNGs properly. This increases the length of operation but is the only solution I could find.
            #(cv2 can read pngs by specifying cv2.IMREAD_UNCHANGED but this is a double edged sword as you lose the EXIF data of the image as well)
            temp_file = np.asarray(ImageOps.exif_transpose(Image.open(file)))
                
            width_px = int((abs(self.width)*img_width)/100) #width of the output picture in pixel
            height_px = int((abs(self.height)*img_height)/100) #height of the output picture in pixel
                
            k = 0 #'k' keeps track of how faces pass the threshold test in an image
            
            if bool_face_count: #only saves the face with the highest confidence, which is the first one in the sorted array
                face_range = range(1)
            else:
                face_range = range(faces.shape[2])
                
            #loop through all the potential faces found the neural network
            for i in face_range:
                confidence = faces[0, 0, i, 2]
                if confidence > self.threshold: #checks if confidence is high enough
                    k+=1
                       
                    box = faces[0, 0, i, 3:7] * np.array([img_width, img_height, img_width, img_height]) #transform face from proportion to pixels
                    face = box.astype("int")
                    x0, y0, x1, y1 = face #coordinates of the face in pixel          
                    h = y1 - y0 #height of face
                    w = x1 - x0 #width of face
                    
                    south = min(int(y0 + 0.5*h + ((50+self.height_asy)/100)*height_px), img_height) #southern border of our new cropped image

                    #makes sure that north and south are not outside the original image
                    if south - height_px < 0 and ext.lower() not in PNGS: 
                        south = height_px
                        north = 0
                    else:
                        north = max(south - height_px, 0)
                    
                    west = max(int(x0 + 0.5*w - ((50+self.width_asy)/100)*width_px), 0) #western border of our new cropped image

                    #makes sure that east and west are not outside the original image
                    if west + width_px > img_width: 
                        west = img_width - width_px
                        east = img_width
                    else:
                        east = min(west + width_px, img_width)
                
                    #crops the new image from the original one
                    face  = temp_file[north : south, west : east]
                    

                    #if image is a PNG, we can add extend the height above the top of the head to make sure every cropped image has the same space above their head. 
                    #This is useful if you have images of tall individuals with very little space between the top of his/her head
                    if ext.lower() in PNGS:
                        extra_height = height_px - min(int(y0 + 0.5*h + ((50+self.height_asy)/100)*height_px), img_height)
                        if extra_height > 0:
                            extra_layer = np.full((extra_height, face.shape[1], 4), 255, dtype='uint8')
                            extra_layer[:, :, 3] = 0 #value of 0 is a white background
                            face = np.concatenate((extra_layer, face), axis=0)
                        
                    cropped_face = Image.fromarray(face)
                    
                    #only looks for the first face it can find if in preview mode
                    if preview:
                        return cropped_face
                        break
                    
                    
                    file_name_folder = file_name.rstrip()

                    #saves the cropped image
                    if bool_folder:                
                        if not os.path.exists('{0}/{1}/{2}'.format(output_path, folder_name, str(file_name_folder))): #checks if directory already exists
                            os.makedirs('{0}/{1}/{2}'.format(output_path, folder_name, str(file_name_folder)))
                        if k==1:
                            cropped_face.save('{0}/{1}/{2}/{2}{3}{4}'.format(output_path, folder_name, str(file_name_folder), self.tag, ext))
                        else:
                            cropped_face.save('{0}/{1}/{2}/{2}{3}_{4}{5}'.format(output_path, folder_name, str(file_name_folder), self.tag, k, ext)) 
                    
                    else:
                        if not os.path.exists('{0}/{1}'.format(output_path, folder_name)): #checks if directory already exists
                            os.mkdir('{0}/{1}'.format(output_path, folder_name))
                        if k==1:
                            cropped_face.save('{0}/{1}/{2}{3}{4}'.format(output_path, folder_name, str(file_name), self.tag, ext))
                        else:
                            cropped_face.save('{0}/{1}/{2}{3}_{4}{5}'.format(output_path, folder_name, str(file_name), self.tag, k,  ext))
                
            #checks if program couldn't find any face for an image. If so, will save the original image in a seperate folder
            if k == 0:
                if preview:
                    pass
                
                else:
                    print('{}: Failed to detect face'.format(file_name))
                    if not os.path.exists('{0}/{1}'.format(output_path, self.failure_folder)):
                        os.mkdir('{0}/{1}'.format(output_path, self.failure_folder))
                    Image.fromarray(temp_file).save('{0}/{1}/{2}{3}'.format(output_path, self.failure_folder, str(file_name), ext))
                
                continue                                           
    

