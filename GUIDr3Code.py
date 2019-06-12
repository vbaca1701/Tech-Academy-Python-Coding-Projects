

import subprocess
import sys
import os
import sqlite3
import shutil
from tkinter import *
from tkinter import filedialog
from tkinter import Tk
from datetime import datetime


txtFilesAbsolutePathList = []
globalCount = []
class SearchBox(Frame):
    def __init__(self, master):
        Frame.__init__(self)

        self.master = master
        self.master.resizable(width=False, height=False)
        self.master.geometry('{}x{}'.format(605, 260))  # (width,height)
        self.master.title('Cut and Paste all .txt files found from one folder to another.')
        self.master.config(bg='#b0e0e6')

# -------------------------------------Row 0-------------------------------------------

        self.btnBrowse1 = Button(
            self.master, text='Browse Source', width=16, height=2, command=self.browseSource)
        self.btnBrowse1.grid(row=0, column=0, padx=(20, 0), pady=(50, 0))

        self.txtBox1 = Entry(self.master, font=(
            'Arial', 10), fg='black', width=58)
        self.txtBox1.grid(row=0, column=1, padx=(30, 0), pady=(50, 0))

# -------------------------------------Row 1-------------------------------------------

        self.lblMsg = Label(self.master, text='Log:', font=(
            'Arial', 10), fg='black', width=10, bg='lightblue')
        self.lblMsg.grid(row=1, column=0, padx=(25, 0), pady=(5, 0))

        self.lblMsg1 = Label(self.master, text='', font=(
            'Arial', 10), fg='black', width=55, bg='#b0e0e6')
        self.lblMsg1.grid(row=1, column=1, padx=(5, 0), pady=(0, 0))

# -------------------------------------Row 2-------------------------------------------

        self.lblMsg2 = Label(self.master, text='', font=(
            'Arial', 10), fg='black', width=55, bg='#b0e0e6')
        self.lblMsg2.grid(row=2, column=1, padx=(5, 0), pady=(0, 20))

# -------------------------------------Row 3-------------------------------------------

        # Row 3 will be added or removed when the browseSource(self) and reset(self) functions are utilized

# -------------------------------------Row 4-------------------------------------------

        self.btnCloseProg = Button(
            self.master, text='Close Program', width=15, height=2, command=self.close)
        self.btnCloseProg.grid(row=4, column=1, sticky=SE)

# ---------------------------------Button Functions--------------------------------------

  
    def browseSource(self):
        test = self.txtBox1.get()
        print("Below is the text the user wrote on textbox 1 before clicking on the 'Browse Source' button: \n'{}'\n".format(test))

        
        test1 = self.txtBox1.delete(0, END)
        print("The text, '{}' has now been deleted for data normalization: \n{}\n".format(
            test, test1))

        
        dirVariable = filedialog.askdirectory()

        self.txtBox1.insert(0, dirVariable)
        # Will have the user select a directory before proceeding 
        if (self.txtBox1.get() == '') or (self.txtBox1.get() == None):
            self.lblMsg1.config(
                bg='#c6e2ff', text='Please select a source directory to proceed...')
            self.lblMsg2.config(
                bg='#b0e0e6', text='')
        else:

            fPath = self.txtBox1.get()
            print('This is the source directory that was selected: \n{}\n'.format(fPath))

            conn = sqlite3.connect('myDatabase1.db')
            with conn:
                cur = conn.cursor()
                cur.execute("CREATE TABLE IF NOT EXISTS tbl_myTxtFiles(\
                    ID INTEGER PRIMARY KEY AUTOINCREMENT, \
                    col_qualifyingFile TEXT,\
                    col_timeStamp TEXT\
                    )")
                conn.commit()
            conn.close()

            # Creates list of files in another directory
            directoryList = os.listdir(fPath)
            print("All files in directory, {} are listed below: \n{}\n".format(
                fPath, directoryList))

            conn = sqlite3.connect('myDatabase1.db')
            with conn:
                cur = conn.cursor()
                count = 0
                print("The text files detected are: ")
                for file in directoryList:
                    if file.endswith('.txt'):
                        # Concatinates the path directory with a txt file found through each iteration.
                        abPath = os.path.join(fPath, file)
                        txtFilesAbsolutePathList.append(abPath)
                        
                        # Will retrieve last modified time
                        fModTime = os.path.getmtime(abPath)
                        formattedTime = datetime.fromtimestamp(fModTime).strftime(
                            '%m-%d-%Y %H:%M:%S')  # Formats the time in an understandable format
                        count += 1  # Increments count by 1 through each iteration.
                        globalCount.insert(0,count)
                        print(
                            "File {}. {} : Last-Modified Time {}".format(count, abPath, formattedTime))
                        cur.execute(
                            "INSERT INTO tbl_myTxtFiles(col_qualifyingFile,col_timeStamp) VALUES (?,?)", (file, formattedTime))
                conn.commit()
            conn.close()

            # This if statement checks if txt files are found, then allow the user to browse a destionation, otherwise don't.
        
            if count == 0:
                try:
                    self.btnBrowse2.grid_remove()
                    self.txtBox2.grid_remove()
                    self.btnGo.grid_remove()
                    self.btnReset.grid_remove()
                    self.lblMsg1.config(
                        bg='lightgreen', text="There are {} .txt files found in the directory you have selected.".format(count))
                    self.lblMsg2.config(
                        bg='lightgreen', text="Please click on the 'Browse Directory...' button to select another path.")
                except:
                    self.lblMsg1.config(
                        bg='lightgreen', text="There are {} .txt files found in the directory you have selected.".format(count))
                    self.lblMsg2.config(
                        bg='lightgreen', text="Please click on the 'Browse Directory...' button to select another path.")
                    print('\nNOTE: There are no button(s) or textbox to remove yet.')
            elif count > 0:
                self.lblMsg1.config(
                    bg='lightgreen', text="{} .txt file(s) have been found in the directory you have selected.".format(count))
                self.lblMsg2.config(
                    bg='lightgreen', text="Press the 'Browse Destination...' to proceed.")

                self.btnBrowse2 = Button(
                    self.master, text='Browse Destination...', width=16, height=2, command=self.browseDestination)
                self.btnBrowse2.grid(row=3, column=0, padx=(20, 0), pady=(0, 0))

                self.txtBox2 = Entry(self.master, font=(
                    'Arial', 10), fg='black', width=58)
                self.txtBox2.grid(row=3, column=1, padx=(30, 0), pady=(0, 0))


    def browseDestination(self):
        if (self.txtBox1.get() == '') or (self.txtBox1.get() == None):
            self.lblMsg1.config(
                bg='lightblue', text="You must first click the 'Browse Source' button to select the source...")
        else:
            # This is done in case the user decided to type something in the textbox before
            # pressing the [Browse Destination...] button.
            test = self.txtBox2.get()
            print("Below is the text the user wrote on textbox 2 before clicking on the 'Browse Destinaton' button: \n'{}'\n".format(test))

            # Deletes chars located in index 0,1,2,3...until END.
            test1 = self.txtBox2.delete(0, END)
            print("The text, '{}' has now been deleted for data normalization: \n{}\n".format(
                test, test1))

            # When this function s called, the window to select a folder pops up. This returns the selected path if there was a selection.
            dirVariable = filedialog.askdirectory()

            self.txtBox2.insert(0, dirVariable)
            # If there are no selections, ask the  user to select a directory to proceed.
            if (self.txtBox2.get() == '') or (self.txtBox1.get() == None):
                self.lblMsg2.config(
                    bg='lightblue', text='Please select a destination directory to proceed...')
            elif (self.txtBox1.get() == self.txtBox2.get()):
                self.lblMsg2.config(
                    bg='lightblue', text='Your destination directory must be different from your source directory.. ')

                self.txtBox2.delete(0, END)
            else:
                self.lblMsg1.config(
                    bg='lightblue', text='')

                self.lblMsg2.config(
                    bg='lightgreen', text="Press 'GO!' to cut and paste .txt files found to the destination directory!")

                self.btnGo = Button(
                    self.master, text='GO!', width=8, height=2, command=self.go)
                self.btnGo.grid(row=4, column=1, sticky=SW, padx=(36,0))

            fPath = self.txtBox2.get()
            print('This is the destination directory that was selected: \n{}\n'.format(fPath))

    def go(self):
        print("The 'GO!' button was pressed.\n")
        try:
            abFilePaths = txtFilesAbsolutePathList
            destination = self.txtBox2.get()

            # shutil.move(src,dst) recursively move a file or directory (src) to another location (dst) and return the destination.
            for file in abFilePaths:
                shutil.move(file, destination) 


            self.lblMsg1.config(
                bg='lightgreen', text="Your {} .txt file(s) found have been moved to your selected directory!".format(globalCount[0]))

            self.lblMsg2.config(
                bg='lightgreen', text="SUCCESS!!")
            
            print("Success!!!")

            self.btnReset = Button(
                self.master, text='Reset', width=16, height=2, command=self.reset)
            self.btnReset.grid(row=4, column=1, padx=(72,0))

            self.btnGo.config(state=DISABLED) # Disables the button to decrease likelyhood of the program malfunctioning
            self.btnBrowse1.config(state=DISABLED)
            self.btnBrowse2.config(state=DISABLED)

            path=os.path.normpath(destination)
            print(path)
            subprocess.Popen(f'explorer {os.path.realpath(path)}')

        except:

            self.lblMsg1.config(
                bg='lightblue', text="ERROR: Please browse a valid source and/or destination.".format(globalCount[0]))

            self.lblMsg2.config(
                bg='lightblue', text="Try pressing the 'Reset' button to restart the process.")

            print("ERROR: Please browse a valid source and/or destination.")

            self.btnReset = Button(
                self.master, text='Reset', width=16, height=2, command=self.reset)
            self.btnReset.grid(row=4, column=1, padx=(72,0))

            self.btnGo.config(state=DISABLED)
            self.btnBrowse1.config(state=DISABLED)
            self.btnBrowse2.config(state=DISABLED)

    def close(self):
        self.master.destroy()

    def reset(self):
        print("\n\nThe 'Reset' button was pressed.")

        self.btnBrowse1.config(state=NORMAL)
        self.txtBox1.delete(0, END)
        self.btnBrowse2.grid_remove()
        self.txtBox2.grid_remove()
        self.lblMsg1.config(
            bg='#b0e0e6', text="")
        self.lblMsg2.config(
            bg='#b0e0e6', text="")
        self.btnGo.grid_remove()
        self.btnReset.grid_remove()
        txtFilesAbsolutePathList.clear()
        globalCount.clear()


if __name__ == "__main__":
    root = Tk()
    App = SearchBox(root)
    root.mainloop()
