#!/usr/bin/python

# http://biostumblematic.wordpress.com

import sys, re, tkFileDialog, string
from Tkinter import *

filelist=[]
recordnames = []

class Gpdbcleaner:
    def __init__(self, root):
        '''Set up the TKinter window'''
        frame = Frame(root)
        frame.pack(fill=BOTH)

        self.openbutton = Button(frame, text='Select PDB file', command=self.openfile)
        self.openbutton.grid(row=0, sticky=W)

	self.openfilename = StringVar()
	self.openfilename.set('')

	self.openfile = Label(frame, width=50, relief=SUNKEN, anchor=W, textvariable=self.openfilename)
	self.openfile.grid(row=0, column=1, sticky=W)

	self.savefilename = StringVar()
	self.savefilename.set('')

        self.savebutton = Button(frame, text='Save As', command=self.asksaveasfilename)
        self.savebutton.grid(row=1, sticky=W)

	self.savefile = Label(frame, width=50, relief=SUNKEN, anchor=W, textvariable=self.savefilename)
	self.savefile.grid(row=1, column=1, sticky=W)

        self.runbutton = Button(frame, text='Run', fg='green', command=self.run)
        self.runbutton.grid(row=2, sticky=W)

        self.quitbutton = Button(frame, text='Quit', fg='red', command=frame.quit)
        self.quitbutton.grid(row=2, column=1, sticky=W)

    def openfile(self):
	self.askopenfilename()
	self.getrecordnames()

    def askopenfilename(self):
        '''Get the name of the PDB file to be cleaned up'''
        dirtyfile = tkFileDialog.askopenfilename()
	self.openfilename.set(dirtyfile)
        return filelist.append(dirtyfile)

    def asksaveasfilename(self):
        '''Get the save as file name'''
        cleanfile = tkFileDialog.asksaveasfilename()
	self.savefilename.set(cleanfile)
        return filelist.append(cleanfile)

    def getrecordnames(self):
	'''Create a list of all the record names in the PDB file'''
        inputfile = open(filelist[0], 'r')
	lines = inputfile.readlines()
	for line in lines:
	    recordmatch = re.match('^\S*', line)
	    record = recordmatch.group()
	    if record in recordnames:
	        pass
	    else:
	        recordnames.append(record)
	inputfile.close()

    def run(self):
        '''Perform the cleanup'''
        atomrecords=[]
        inputfile = open(filelist[0], 'r')
        lines = inputfile.readlines()
        for line in lines:
            match = re.search('^ATOM', line)
            if match:
                atomrecords.append(line)
            else:
                pass
        atomrecords.append('END')
        inputfile.close()

        # Write out the records
        outputfile = open(filelist[1], 'w')
        outputfile.writelines(atomrecords)
        outputfile.close()

root = Tk()
root.title('PDB cleaner')

gpdbcleaner = Gpdbcleaner(root)

root.mainloop()
