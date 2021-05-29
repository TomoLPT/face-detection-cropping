# -*- coding: utf-8 -*-
#author: Tomo Lapautre

import glob
import os
from PIL import ImageQt
from itertools import compress
import json
# import time

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

from main.facecrop import FaceCrop
            

param_file_path = 'main/parameters.json' #file used to save cropping preferences

#autorisation to open and write the parameters file is restricted if the GUI is installed in :C/ProgramFiles directory
#user has to execute the GUI in admin mode or GUI will crash
#to avoid crashing, code below tests if access is restricted
try:
    parameters_json = open(param_file_path)
    parameters = json.load(parameters_json)
    autorisation = True 
except:
    autorisation = False
    print("No autorisation to read parameters.json")
 

#GUI design, standard pyqt5 code
class Ui_MainWindow(object): 
    def __init__(self, language):
        self.language = language

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(778, 883)
        # MainWindow.setWindowIcon(QtGui.QIcon('logo.ico'))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.title = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.title.sizePolicy().hasHeightForWidth())
        self.title.setSizePolicy(sizePolicy)
        self.title.setMinimumSize(QtCore.QSize(0, 100))
        font = QtGui.QFont()
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setObjectName("title")


        self.verticalLayout.addWidget(self.title, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.input_dir_button = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.select_input_dir())
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.input_dir_button.sizePolicy().hasHeightForWidth())
        self.input_dir_button.setSizePolicy(sizePolicy)
        self.input_dir_button.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.input_dir_button.setFont(font)
        self.input_dir_button.setObjectName("input_dir_button")
        self.verticalLayout.addWidget(self.input_dir_button, 0, QtCore.Qt.AlignHCenter)


        self.output_dir_button = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.select_output_dir())
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.output_dir_button.sizePolicy().hasHeightForWidth())
        self.output_dir_button.setSizePolicy(sizePolicy)
        self.output_dir_button.setMinimumSize(QtCore.QSize(200, 0))
        self.output_dir_button.setFont(font)
        self.output_dir_button.setObjectName("output_dir_button")
        self.verticalLayout.addWidget(self.output_dir_button, 0, QtCore.Qt.AlignHCenter)


        self.BOX = QtWidgets.QWidget(self.centralwidget)
        self.BOX.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.BOX.sizePolicy().hasHeightForWidth())
        self.BOX.setSizePolicy(sizePolicy)
        self.BOX.setMinimumSize(QtCore.QSize(0, 0))
        self.BOX.setObjectName("BOX")


        self.gridLayout = QtWidgets.QGridLayout(self.BOX)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.gridLayout.setContentsMargins(50, -1, 50, -1)
        self.gridLayout.setHorizontalSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        
        self.width_asy_label = QtWidgets.QLabel(self.BOX)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.width_asy_label.sizePolicy().hasHeightForWidth())
        self.width_asy_label.setSizePolicy(sizePolicy)
        self.width_asy_label.setFont(font)
        self.width_asy_label.setObjectName("width_asy_label")
        self.gridLayout.addWidget(self.width_asy_label, 0, 2, 1, 1, QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        
        self.height_label = QtWidgets.QLabel(self.BOX)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.height_label.sizePolicy().hasHeightForWidth())
        self.height_label.setSizePolicy(sizePolicy)
        self.height_label.setFont(font)
        self.height_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.height_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.height_label.setObjectName("height_label")
        self.gridLayout.addWidget(self.height_label, 3, 0, 1, 1, QtCore.Qt.AlignRight)
        
        self.tag_label = QtWidgets.QLabel(self.BOX)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tag_label.sizePolicy().hasHeightForWidth())
        self.tag_label.setSizePolicy(sizePolicy)
        self.tag_label.setFont(font)
        self.tag_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.tag_label.setObjectName("tag_label")
        self.gridLayout.addWidget(self.tag_label, 4, 0, 1, 1, QtCore.Qt.AlignRight)
        
        self.tag_input = QtWidgets.QLineEdit(self.BOX)
        self.tag_input.setMaximumSize(QtCore.QSize(150, 16777215))
        self.tag_input.setObjectName("tag_input")
        self.gridLayout.addWidget(self.tag_input, 4, 1, 1, 1, QtCore.Qt.AlignLeft)
        font_input = QtGui.QFont()
        font_input.setBold(True)
        font_input.setWeight(75)
        font_input.setPointSize(10)
        self.tag_input.setFont(font_input)
        
        self.height_asy_label = QtWidgets.QLabel(self.BOX)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.height_asy_label.sizePolicy().hasHeightForWidth())
        self.height_asy_label.setSizePolicy(sizePolicy)
        self.height_asy_label.setFont(font)
        self.height_asy_label.setObjectName("height_asy_label")
        self.gridLayout.addWidget(self.height_asy_label, 3, 2, 1, 1, QtCore.Qt.AlignRight)

        self.height_asy_input = QtWidgets.QLineEdit(self.BOX)
        self.height_asy_input.setMaximumSize(QtCore.QSize(150, 16777215))
        self.height_asy_input.setText('0')
        self.height_asy_input.setObjectName("height_asy_input")
        self.height_asy_input.setFont(font_input)
        self.gridLayout.addWidget(self.height_asy_input, 3, 3, 1, 1, QtCore.Qt.AlignLeft)
        
        self.width_asy_input = QtWidgets.QLineEdit(self.BOX)
        self.width_asy_input.setMaximumSize(QtCore.QSize(150, 16777215))
        self.width_asy_input.setText('0')
        self.width_asy_input.setObjectName("width_asy")
        self.width_asy_input.setFont(font_input)
        self.gridLayout.addWidget(self.width_asy_input, 0, 3, 1, 1, QtCore.Qt.AlignLeft)

        self.height_input = QtWidgets.QLineEdit(self.BOX)
        self.height_input.setMaximumSize(QtCore.QSize(150, 16777215))
        self.height_input.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.height_input.setAutoFillBackground(False)
        self.height_input.setFrame(True)
        self.height_input.setObjectName("height_input")
        self.height_input.setText('60')
        self.height_input.setFont(font_input)
        self.gridLayout.addWidget(self.height_input, 3, 1, 1, 1, QtCore.Qt.AlignLeft)

        self.width_label = QtWidgets.QLabel(self.BOX)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.width_label.sizePolicy().hasHeightForWidth())
        self.width_label.setSizePolicy(sizePolicy)
        self.width_label.setFont(font)
        self.width_label.setObjectName("width_label")
        self.gridLayout.addWidget(self.width_label, 0, 0, 1, 1, QtCore.Qt.AlignRight)

        self.width_input = QtWidgets.QLineEdit(self.BOX)
        self.width_input.setText('60')
        self.width_input.setMaximumSize(QtCore.QSize(150, 16777215))
        self.width_input.setObjectName("width_input")
        self.width_input.setFont(font_input)
        self.gridLayout.addWidget(self.width_input, 0, 1, 1, 1, QtCore.Qt.AlignLeft)
        self.verticalLayout.addWidget(self.BOX)


        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(100, -1, 100, -1)
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.checkbox_folder = QtWidgets.QCheckBox(self.centralwidget)
        self.checkbox_folder.setChecked(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkbox_folder.sizePolicy().hasHeightForWidth())
        self.checkbox_folder.setSizePolicy(sizePolicy)
        self.checkbox_folder.setFont(font)
        self.checkbox_folder.setObjectName("checkbox_folder")
        self.horizontalLayout.addWidget(self.checkbox_folder, 0, QtCore.Qt.AlignRight)

        self.checkbox_count = QtWidgets.QCheckBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkbox_count.sizePolicy().hasHeightForWidth())
        self.checkbox_count.setSizePolicy(sizePolicy)
        self.checkbox_count.setFont(font)
        self.checkbox_count.setObjectName("checkbox_count")
        self.checkbox_count.setChecked(True)
        self.horizontalLayout.addWidget(self.checkbox_count, 0, QtCore.Qt.AlignLeft)
        self.verticalLayout.addLayout(self.horizontalLayout)


        self.preview_button = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.crop(preview=True))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.preview_button.sizePolicy().hasHeightForWidth())
        self.preview_button.setSizePolicy(sizePolicy)
        self.preview_button.setMinimumSize(QtCore.QSize(200, 0))
        self.preview_button.setFont(font)
        self.preview_button.setObjectName("preview_button")
        self.verticalLayout.addWidget(self.preview_button, 0, QtCore.Qt.AlignHCenter)
        

        self.preview_image = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.preview_image.sizePolicy().hasHeightForWidth())
        self.preview_image.setSizePolicy(sizePolicy)
        self.preview_image.setMinimumSize(QtCore.QSize(0, 300))
        self.preview_image.setAutoFillBackground(True)
        self.preview_image.setStyleSheet("QLabel {background: white}")
        self.preview_image.setFrameShape(QtWidgets.QFrame.Box)
        self.preview_image.setFrameShadow(QtWidgets.QFrame.Raised)
        self.preview_image.setLineWidth(2)
        self.preview_image.setText("")
        self.preview_image.setObjectName("preview_image")
        self.verticalLayout.addWidget(self.preview_image)
        
        
        self.crop_button = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.crop(preview=False))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.crop_button.sizePolicy().hasHeightForWidth())
        self.crop_button.setSizePolicy(sizePolicy)
        self.crop_button.setMinimumSize(QtCore.QSize(200, 50))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.crop_button.setFont(font)
        self.crop_button.setObjectName("crop_button")
        self.verticalLayout.addWidget(self.crop_button, 0, QtCore.Qt.AlignHCenter)


        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 778, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.title.setBuddy(self.BOX)

        #loads parameters if app managed to load parameters.json file
        if autorisation: 
            self.tag_input.setText(parameters['tag'])
            self.height_asy_input.setText(str(parameters['height_asy']))
            self.width_asy_input.setText(str(parameters['width_asy']))
            self.height_input.setText(str(parameters["height"]))
            self.height_input.setText(str(parameters["height"]))
            self.width_input.setText(str(parameters['width']))
            self.checkbox_folder.setChecked(parameters['folder_option'])
            self.checkbox_count.setChecked(parameters['single_face_option'])


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate

        if self.language == "french":
            MainWindow.setWindowTitle("Cadrage Automatique")
            self.title.setText(_translate("MainWindow", "Cadrage Automatique"))
            self.input_dir_button.setText(_translate("MainWindow", "Dossier des Images"))
            self.output_dir_button.setText(_translate("MainWindow", "Dossier de Sortie"))
            self.width_asy_label.setText(_translate("MainWindow", "Assymétrie Horizontale (%)"))
            self.height_label.setText(_translate("MainWindow", "Hauteur (%)"))
            self.tag_label.setText(_translate("MainWindow", "Tag Fichier"))
            self.height_asy_label.setText(_translate("MainWindow", "Assymétrie Verticale (%)"))
            self.width_label.setText(_translate("MainWindow", "Largeur (%)"))
            self.checkbox_folder.setText(_translate("MainWindow", "Créer un dossier par individu?"))
            self.checkbox_count.setText(_translate("MainWindow", "Un visage par photo?"))
            self.preview_button.setText(_translate("MainWindow", "Aperçu"))
            self.crop_button.setText(_translate("MainWindow", "Rogner"))

            self.warning_values = 'Valeurs non reconnues'
            self.warning_folders = "Veuillez indiquer un dossier d'entrée et de sortie"
            self.warning_title = 'Erreur'
            self.warning_no_file = 'Votre dossier est vide'

        if self.language == "english":
            MainWindow.setWindowTitle("Face Crop")
            self.title.setText(_translate("MainWindow", "Face Detection Cropping"))
            self.input_dir_button.setText(_translate("MainWindow", "Input Folder"))
            self.output_dir_button.setText(_translate("MainWindow", "Output Folder"))
            self.width_asy_label.setText(_translate("MainWindow", "Horizontal Assymmetry (%)"))
            self.height_label.setText(_translate("MainWindow", "Height (%)"))
            self.tag_label.setText(_translate("MainWindow", "File Tag"))
            self.height_asy_label.setText(_translate("MainWindow", "Vertical Assymmetry (%)"))
            self.width_label.setText(_translate("MainWindow", "Width (%)"))
            self.checkbox_folder.setText(_translate("MainWindow", "Create one folder per face?"))
            self.checkbox_count.setText(_translate("MainWindow", "My images contain only one individual"))
            self.preview_button.setText(_translate("MainWindow", "Preview"))
            self.crop_button.setText(_translate("MainWindow", "Frame"))

            self.warning_folders = 'Please specify an input and output folder'
            self.warning_values = 'Input values not recognised'
            self.warning_title = 'Error'
            self.warning_no_file = 'Your input folder is empty'
        

    #function to load input directory    
    def select_input_dir(self):
        self.input_path = QtWidgets.QFileDialog.getExistingDirectory()
        self.paths = glob.glob('{}/*'.format(self.input_path))
        if len(self.paths)==0:
            print("No files in folder!")
            self.error_popup(self.warning_no_file)
        
    #function to load output directory
    def select_output_dir(self):
        self.output_path = QtWidgets.QFileDialog.getExistingDirectory()
        
    
    #main function executed when Frame button is pressed
    def crop(self, preview=False): #preview means we only want to generate the first picture we find. Activated when Preview button is pressed
        
        #making sure data entered in each field is of correct format
        try: 
            height = float(self.height_input.text())
            width = float(self.width_input.text())
            height_asy = float(self.height_asy_input.text())
            width_asy = float(self.width_asy_input.text())
            tag = str(self.tag_input.text())
            bool_folder = self.checkbox_folder.isChecked()
            bool_face_count = self.checkbox_count.isChecked()

            face_crop = FaceCrop(height, width, height_asy, width_asy, tag, pyqt_ui=self) #initialising instance of the FaceCrop class
        
        #if incorrect, popup appears
        except:
            self.error_popup(self.warning_values) 
            return

        #saves preferences if app is autorised to write file
        if autorisation: 
            self.update_params(parameters, param_file_path) 
        
        #making sure input and output path were defined by the user
        try: 
            self.input_path
            self.output_path 
            bool_folders = [os.path.isdir(i) for i in self.paths]
            subfolders = any(bool_folders) #subfolders variable checks if input directory contains folders that need to be treated
            
        except:
            self.error_popup(self.warning_folders)
            return        


        #if subfolders if true, program will convert images found in those subfolders
        if subfolders:
            
            directories = list(compress(self.paths, bool_folders)) #finds all the subfolders
            bar_length = sum([len(next(os.walk(dir_))[2]) for dir_ in directories]) #calculates the bar length of our progress bar
            
            #initialises a progress bar if we are not generating just a preview image
            if not preview: 
                self.progress_bar(bar_length)

            #checks images in all subfolders
            for directory in directories: 
                if preview:
                    preview_img = face_crop.crop_save(directory, self.output_path, bool_folder=bool_folder, bool_face_count=bool_face_count, preview=preview)
                else:
                    if self.progress.wasCanceled(): #breaks program if user clicked on the 'cancel' button of the progress bar
                        break
                    face_crop.crop_save(directory, self.output_path, bool_folder=bool_folder, bool_face_count=bool_face_count)
        
        
        else:
            bar_length = len(next(os.walk(self.input_path))[2])

            if preview:
                preview_img = face_crop.crop_save(self.input_path, self.output_path, bool_folder=bool_folder, 
                                                  bool_face_count=bool_face_count, preview=preview)
            else:
                self.progress_bar(bar_length)
                face_crop.crop_save(self.input_path, self.output_path, bool_folder=bool_folder, 
                                    bool_face_count=bool_face_count)
    

        #displays preview image if preview is true
        if preview:
            imgQ = ImageQt.ImageQt(preview_img)
            
            pixMap = QtGui.QPixmap.fromImage(imgQ)
            
            self.preview_image.setPixmap(pixMap.scaled(self.preview_image.width(), 
                                                    self.preview_image.height(), 
                                                    QtCore.Qt.KeepAspectRatio))
            self.preview_image.setAlignment(QtCore.Qt.AlignCenter)
        
    
    #method to display a message in a popup
    def error_popup(self, text):
         self.msg = QtWidgets.QMessageBox()
         self.msg.setWindowTitle(self.warning_title)
         self.msg.setText(text)
         self.msg.setIcon(QtWidgets.QMessageBox.Critical)
         self.msg.exec_()        


    #method to generate progress_bar
    def progress_bar(self, length):
        self.progress = QtWidgets.QProgressDialog("Veuillez Patienter", "Annuler", 0, length)
        self.progress.setWindowModality(Qt.WindowModal)
        self.progress.setWindowTitle("Cadrage en cours")
        self.progress.setFixedSize(600, 100)
        self.progress.setMinimumDuration(100)


    #method to update parameters by writing variables values in the parameters.json file
    def update_params(self, data, file_name):

        data['width'] = self.width_input.text()
        data['height'] = self.height_input.text()
        data['width_asy'] = self.width_asy_input.text()
        data['height_asy'] = self.height_asy_input.text()
        data['tag'] = self.tag_input.text()
        data['folder_option'] = self.checkbox_folder.isChecked()
        data['big_face_option'] = self.checkbox_count.isChecked()
        
        with open(file_name, 'w') as outfile:
            json.dump(data, outfile)

        
            

def main(app_language):
    # if time.time() < 1628438147:
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(app_language)
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

    
    
    


