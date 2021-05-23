# face-detection-cropping

A GUI to automatically batch crop your portraits using face detection.

## Installation
To use this GUI, you can either:
1. Download the source code and generate the executable through the run.spec file using pysintaller
~~~sh
pyinstaller run.spec
~~~
2. Download the "dist" directory which contains the already packaged executable (your antivirus software might cause issues as the GUI is not signed)

The opencv DNN algorithm is used to detect faces. 

## Use
![Alt text](https://github.com/TomoLPT/face-detection-cropping/blob/main/readme_images/app.JPG?raw=true "GUI")

Buttons:
* **Input Folder**: Directory containing the  images. If the input direcotry contains at least one folder, the program will search images inside those subfolders
* **Output Folder**: Directory where the cropped images will be saved
* **Preview**: A preview of what the cropped image will look like. Used to calibrate the cropping parameters. Takes the first image in the directory where a face was successfully detected.
* **Frame**: Crops all the images in the input folder.

Entry Fields:
* **Width (%)**: The width of the cropped image, expressed as a percentage of the initial image width. (Int between 0 and 100)
* **Height (%)**: The height of the cropped image, expressed as a percentage of the initial image height. (Int between 0 and 100)
* **Horizontal Assymmetry (%)**: The horizontal assymmetry of the cropped area relative to the position of the face, expressed as a percentage of the initial image width. A value of 0 will output a perfectly horizontally centered image. A positive value will shift the image to the left of the face. A negative value will shift the image to the right(Integers)
* **Vertical Assymmetry (%)**: The vertical assymmetry of the cropped area relative to the position of the face, expressed as a percentage of the initial image height. A value of 0 will output a perfectly vertically centered image. A positive value will shift the image down from the face. A negative value will shift the image up (Integers)
![Alt text](https://github.com/TomoLPT/face-detection-cropping/blob/main/readme_images/illustration.JPG?raw=true "GUI")
* **File Tag**: The program will save the cropped image with its original name + the file tag. Ex: IMG001 is saved as IMG001_A for a file tag of 'A'.

Checkboxes:
* **Create one folder per face?**: save the cropped image in its own folder. Ex: IMG001 is saved in folder named IMG001.
* **My images contain only one individual**: Only finds the face with the highest confidence in each image. Otherwise can crop multiple face in an image.

## Example:
* **Width (%)**: 35
* **Height (%)**: 70
* **Horizontal Assymmetry (%)**: 0
* **Vertical Assymmetry (%)**: 0

![Alt text](https://github.com/TomoLPT/face-detection-cropping/blob/main/readme_images/example_1.JPG?raw=true "GUI")


* **Width (%)**: 55
* **Height (%)**: 80
* **Horizontal Assymmetry (%)**: 15
* **Vertical Assymmetry (%)**: 5

![Alt text](https://github.com/TomoLPT/face-detection-cropping/blob/main/readme_images/example_2.JPG?raw=true "GUI")

## Supported image file types

* JPG (tested)
* PNG (tested)
* Any image file readable by opencv and Pillow (not tested)

## Supported languages

* english
* french

You can modify the language in the run.py file:

~~~python
if __name__ == "__main__":
    main('english') #'english' or 'french' supported
~~~
	
## Credits
Adapted from:
* https://github.com/leblancfg/autocrop
* https://towardsdatascience.com/face-detection-models-which-to-use-and-why-d263e82c302c
* https://towardsdatascience.com/detecting-faces-with-python-and-opencv-face-detection-neural-network-f72890ae531c
