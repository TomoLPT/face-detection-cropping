# face-detection-cropping

A GUI to automatically batch crop your portraits using face detection.

To use this GUI, you can either:
	1. download the source code and generate the executable through the run.spec file using pysintaller
		~~~sh
		pyinstaller run.spec
		~~~
	2. Download the "dist" directory which contains the already packaged executable (your antivirus software might cause issues as GUI is not signed)

The opencv DNN algorithm is used to detect faces. 

# Use
![Alt text](./readme_images/app.jpg?raw=true "GUI")


##Supported image file types

* JPG (tested)
* PNG (tested)
* Any image file readable by opencv and Pillow (not tested)

##Supported languages

* english
* french

You can modify the language in the run.py file:

~~~python
if __name__ == "__main__":
    main('english') #'english' or 'french' supported
~~~
	
##Credits
Adapted from:
* https://github.com/leblancfg/autocrop
* https://towardsdatascience.com/face-detection-models-which-to-use-and-why-d263e82c302c
* https://towardsdatascience.com/detecting-faces-with-python-and-opencv-face-detection-neural-network-f72890ae531c
