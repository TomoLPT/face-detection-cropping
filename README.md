# face-detection-cropping

A GUI to automatically batch crop your portraits using face detection. Powered by the OpenCV DNN algorithm.

## Installation
To use this GUI, first download this repo by either:
* cloning this repo from your cmd (install git first):
~~~sh
git clone https://github.com/TomoLPT/face-detection-cropping
~~~
* downloading the zip of this repo 

To execute the GUI, you can either:
1. Start the 'run.py' file (requires python 3)
~~~sh
python run.py
~~~
2. Generate the executable using pyinstaller and the .spec file available in the repo (requires python 3)
~~~sh
pyinstaller run.spec
~~~
3. If you are on Windows: download the "dist" folder of this repo which contains the already packaged executable (your antivirus software might cause issues as the GUI is not signed)

## Use
![Alt text](https://github.com/TomoLPT/face-detection-cropping/blob/main/readme_images/app.JPG?raw=true "Batch Crop GUI")

#### Buttons:
* **Input Folder**: Directory containing the  images. If the input direcotry contains at least one folder, the program will search images inside those subfolders
* **Output Folder**: Directory where the cropped images will be saved
* **Preview**: A preview of what the cropped image will look like. Used to calibrate the cropping parameters. Takes the first image in the directory where a face was successfully detected.
* **Frame**: Crops all the images in the input folder and saves them in the ouput directory.

#### Entry Fields:
![Alt text](https://github.com/TomoLPT/face-detection-cropping/blob/main/readme_images/illustration.JPG?raw=true "Parameters to specify")
* **Width (%)**: The width of the cropped image, expressed as a percentage of the initial image width. (Int between 0 and 100)
* **Height (%)**: The height of the cropped image, expressed as a percentage of the initial image height. (Int between 0 and 100)
* **Horizontal Assymmetry (%)**: The horizontal assymmetry of the cropping area relative to the position of the face. Positive values will shift the image to the left of the face and negative values to the right (Integers). See examples below.
* **Vertical Assymmetry (%)**: The vertical assymmetry of the cropped area relative to the position of the face. Positive values will shift the image down from the face and negative values will shift the image up (Integers). See examples below.
* **File Tag**: The program will save the cropped image with its original file name + the file tag. Ex: IMG001 is saved as IMG001_A for a file tag of 'A'. Optional.

#### Checkboxes:
* **Create one folder per face?**: save the cropped image in its own folder. Ex: IMG001 is saved in a new folder named IMG001. Useful if you have multiple faces in a single image.
* **My images contain only one individual**: Only crops the face with the highest confidence in each image. Otherwise can crop multiple face from a single image.

## Examples:
![Alt text](https://github.com/TomoLPT/face-detection-cropping/blob/main/readme_images/example_1.JPG?raw=true "Example 1")
* Width (%): 55
* Height (%): 80
* Horizontal Assymmetry (%): 15
* Vertical Assymmetry (%): 5
<br/>
<br/>
<br/>

![Alt text](https://github.com/TomoLPT/face-detection-cropping/blob/main/readme_images/example_2.JPG?raw=true "Example 2")
* Width (%): 35
* Height (%): 70
* Horizontal Assymmetry (%): 0
* Vertical Assymmetry (%): 0

## Supported image file types

* JPG (tested)
* PNG (tested)
* Any image file readable by OpenCV and Pillow (not tested)

## Supported OS

* Windows 10 (tested). Should work fine on previous windows versions.
* For other OS, you can generate the executable from your own OS:
~~~sh
pyinstaller run.spec
~~~

## Supported GUI languages

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
