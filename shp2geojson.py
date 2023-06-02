import geopandas
import tkinter
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import os
import zipfile
import shutil
import patoolib


class SHP2GEOJSON:

    def __init__(self):
        # later define input folder name
        self.root = tkinter.Tk().hide()
        self.message = "No shp file/Output file wrong"

    def __get_In_Out_filename(self):
        self.filename = self.__askFile()
        self.outfileName = self.filename.split("/")[-1]

    def __askFile(self):
        self.infileName = askopenfilename(title="Secect shp file", filetypes=(("shp files", "*.shp"), ("all files", "*.*")))
        return self.infileName

    def __warning_message(self):
        messagebox.warning("Warning", self.message)

    def __read_shp2geojson(self):
        self.data = geopandas.read_file(self.filename)
        return self.data

    def __save2geojson(self):
        # get single shp file name

        if self.filename[-3:] in ["shp"]:
            self.geojsonData = self.__read_shp2geojson()
            self.geojsonData.to_file(
                f"""{self.outdir}\{self.outfileName}.geojson""", driver='GeoJSON')
            # Here track file path
            # self.root.destroy()    # close all window degets
            self.root.withdraw()   # hide Tk() window

    def convert_shp_single(self):
        self.__get_In_Out_filename()
        self.outdir = tkinter.filedialog.askdirectory(title="Choose output folder")
        self.__save2geojson()

    # Multiple folder and zip and rar input ###
    def convert_shp_multiple(self):
        # Get input folder name
        self.dirName = tkinter.filedialog.askdirectory(title="Select Input Folder")

        # Get output folder name
        self.outdir = tkinter.filedialog.askdirectory(title="Choose Output Folder")

        self.root.withdraw()
        self.all_file_names = self.__getListOfFilesNames_folder()
        try:
            for name in self.all_file_names:
                self.filename = name
                self.outfileName = name.replace("\\","/").split("/")[-1]
                self.__save2geojson()
        except Exception as err:
            print(err)
            #messagebox.showerror("Warning!",err)

    def __getListOfFilesNames_folder(self):
        self.listOfFilesNames = os.listdir(self.dirName)
        self.allFilesNames = []

        # Iterate over all the entries
        for entry in self.listOfFilesNames:
            self.fullPath = os.path.join(self.dirName, entry)       # Create full path
            if os.path.isdir(self.fullPath):      # If entry is a directory then get the list of files in this directory
                self.dirName = self.fullPath
                self.allFilesNames = self.allFilesNames + self.__getListOfFilesNames_folder()
            else:
                self.allFilesNames.append(self.fullPath)

        return self.allFilesNames

    def __unzip(self):
        # unzip the zip file to a new template folder
        self.temp_folder = "temp_folder"
        self.zipfilename = askopenfilename(filetypes=(("zip files","*.zip"),("all files","*.*")))
        self.root.withdraw()

        self.temp_path = os.getcwd()+"\%s"%self.temp_folder

        with zipfile.ZipFile(self.zipfilename, 'r') as zip_ref:
            zip_ref.extractall(self.temp_path)

    def __del_unzip(self):   # delete the unziped templete folder
        self.temp_folder = "temp_folder"
        shutil.rmtree(r"%s\%s"%(os.getcwd(),self.temp_folder))

    def convert_shp_multiple_zip(self):
        self.__unzip()

        self.dirName = self.temp_path
        self.outdir = tkinter.filedialog.askdirectory(title="Choose Output Folder")
        self.all_file_names = self.__getListOfFilesNames_folder()
        try:
            for name in self.all_file_names:
                self.filename = name
                self.outfileName = name.replace("\\","/").split("/")[-1]
                self.__save2geojson()
        except Exception as err:
            print(err)
            # messagebox.showerror("Warning!",err)
        self.__del_unzip()

    def __unrar(self):     ##unzip the zip file to a new tmeplete folder
        self.rarfilename = askopenfilename(
            title="Select rar file", filetypes=(("rar files","*.rar"),("all files","*.*")))
        self.temp_folder = "temp_folder"
        os.mkdir(self.temp_folder)         # create a temple folder
        self.root.withdraw()
        self.temp_path = os.getcwd() + "\%s" % self.temp_folder
        patoolib.extract_archive(self.rarfilename, outdir="%s\\%s"%(os.getcwd(),self.temp_folder))

    def __del_unrar(self):   ## delete the unziped templete folder
        # self.ttt = self.unrar()
        # self.temp_folder = str(self.ttt.split(".")[0])
        shutil.rmtree(r"%s\%s"%(os.getcwd(),self.temp_folder))

    def convert_shp_multiple_rar(self):
        self.__unrar()

        self.dirName = self.temp_path
        self.outdir = tkinter.filedialog.askdirectory(title="Choose Output Folder")
        self.root.withdraw()
        self.all_file_names = self.__getListOfFilesNames_folder()
        try:
            for name in self.all_file_names:
                self.filename = name
                self.outfileName = name.replace("\\","/").split("/")[-1]
                self.__save2geojson()
        except Exception as err:
            print(err)
            # messagebox.showerror("Warning!",err)

        self.__del_unrar()


if __name__ == "__main__":
    SHP2GEOJSON().convert_shp_multiple_rar()
    # shp2geojson.convert_shp_multiple_zip()
    # shp2geojson.convert_shp_multiple()
    # shp2geojson.convert_shp_single()