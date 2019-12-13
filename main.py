#!/bin/python

import tkinter
import os
import subprocess
import math
from PIL import Image, ImageTk, JpegImagePlugin

MODE_SCALE=0
MODE_FILL=1
MODE_MAX=2
MODE_CENTRE=3
MODE_TILE=4

BACKGROUND_COL='#ffffff'

DIRECTORY=os.path.expanduser('~/Wallpaper')
I3_CONFIG=os.path.expanduser('~/.config/i3/config')

def SanitiseFilename(utText):
	# TO DO: sanitise a filename and return a good version
	return utText

def Elide(stText, psLength = 0):
	# elide a piece of text so that it's no wider than psLength pixels
	# return the elided text
	MAXLEN=17
	if len(stText) > MAXLEN:
		stText = stText[0:MAXLEN] + '...'
	return stText

# redraw on events: resize/reflow, files changed in dir, selection changes
def UpdatePicker():
	cwPicker.update_idletasks()
	# set loop variables
	psCanvasWidth = cwPicker.winfo_width()
	psIconWidth = 170	# total width including highlight but not text
	psIconHeight = 120	# total height including highlight but not text
	psTextHeight = 20
	psPadWidth = 1
	psPadHeight = 15
	scIconsPerRow = math.floor(psCanvasWidth / psIconWidth)
	ixCol = 0
	ixRow = 0
	# draw bits
	temp0 = tkinter.Label(fwPicker, text="Hello!\nHello2!\nHello3!\nHello4!")
	temp0.grid(row=0)
	temp1 = tkinter.Label(fwPicker, text="Hello!\nHello2!\nHello3!\nHello4!")
	temp1.grid(row=1)
	temp2 = tkinter.Label(fwPicker, text="Hello!\nHello2!\nHello3!\nHello4!")
	temp2.grid(row=2)
	temp3 = tkinter.Label(fwPicker, text="Hello!\nHello2!\nHello3!\nHello4!")
	temp3.grid(row=3)
	temp4 = tkinter.Label(fwPicker, text="Hello!\nHello2!\nHello3!\nHello4!")
	temp4.grid(row=4)
	temp5 = tkinter.Label(fwPicker, text="Hello!\nHello2!\nHello3!\nHello4!")
	temp5.grid(row=5)
	temp6 = tkinter.Label(fwPicker, text="Hello!\nHello2!\nHello3!\nHello4!")
	temp6.grid(row=6)
	temp7 = tkinter.Label(fwPicker, text="Hello!\nHello2!\nHello3!\nHello4!")
	temp7.grid(row=7)
	temp8 = tkinter.Label(fwPicker, text="Hello!\nHello2!\nHello3!\nHello4!")
	temp8.grid(row=8)
	temp9 = tkinter.Label(fwPicker, text="Hello!\nHello2!\nHello3!\nHello4!")
	temp9.grid(row=9)
	temp10 = tkinter.Label(fwPicker, text="Hello!\nHello2!\nHello3!\nHello4!")
	temp10.grid(row=10)
	temp11 = tkinter.Label(fwPicker, text="Hello!\nHello2!\nHello3!\nHello4!")
	temp11.grid(row=11)
	temp12 = tkinter.Label(fwPicker, text="Hello!\nHello2!\nHello3!\nHello4!")
	temp12.grid(row=12)
	temp13 = tkinter.Label(fwPicker, text="Hello!\nHello2!\nHello3!\nHello4!")
	temp13.grid(row=13)

	# scan directory
	if not os.path.exists(DIRECTORY):
		os.makedirs(DIRECTORY, exist_ok=True)
	arFiles = sorted(os.listdir(DIRECTORY))
	for fnImage in arFiles:
		# create highlight frame
		print(fnImage)
		ixCol = ixCol + 1
		ixCol = ixCol % scIconsPerRow
		if ixCol == 0:
			ixRow = ixRow + 1

#	for fnImage in arFiles:
#		# create a thumbnail of fnImage and draw on canvas - process symlinks correctly
#		# make clickable :o on click, set svSelectedFile and redraw
#		imThumb = None
#		JpegImagePlugin.DEBUG = True
#		try:
#			fnReal = os.path.realpath(DIRECTORY + '/' + fnImage)
#			print(fnReal)
#			imThumb = Image.open(fnReal)
#			imThumb.thumbnail((psIconWidth, psIconHeight), Image.ANTIALIAS)
#			imTkThumb = ImageTk.PhotoImage(imThumb)
#			lwIcon = tkinter.Label(cwPicker, image=imTkThumb)
#		except OSError:
#			print("OS error! " + fnReal)
# OSError: can't identify file type
#			lwIcon = tkinter.Label(cwPicker, text="image not found")
#		except:
#			print("other exception!")
#		lwIcon.grid(row=ixRow, column=ixCol)
#		# show trimmed down filename
#		stTrimmed = SanitiseFilename(fnImage)
#		fwName = tkinter.Frame(cwPicker, width=psIconWidth, height=psTextHeight + psSpacer)
#		fwName.grid(row=ixRow+1, column=ixCol)
#		fwName.grid_propagate(False) # weird hackery needed just so we can force constraints on widgets :(
#
#		twName = tkinter.Text(fwName, borderwidth=0, highlightthickness=0)
#		twName.insert(tkinter.END, Elide(stTrimmed))
#		twName.grid(row=0, column=0)
#		twName.config(state=tkinter.DISABLED)
#
#		# if selected, draw a border on it
#		svSelectedFile.set(fnImage)
#		if fnImage == svSelectedFile.get():
#			cwPicker.create_line(ixCol * psIconWidth, ixRow * psIconHeight, ixCol * psIconWidth, (ixRow + 1) * psIconHeight, fill="red")
#			cwPicker.create_line((ixCol + 1) * psIconWidth, ixRow * psIconHeight, (ixCol + 1) * psIconWidth, (ixRow + 1) * psIconHeight, fill="red")
#
#	# also on favourites (recent ones in sequence) - read sqlite db
#	# ...?

def Close():
	wwMain.destroy()

def FileHasLine(fnFile, stCheck):
	with open(fnFile, "r") as fpFile:
		for stLine in fpFile:
			if stCheck in stLine:
				return True
	return False

def AppendFileWithLine(fnFile, stLine):
	with open(fnFile, "a") as fpFile:
		fpFile.write(stLine + "\n")

def WriteI3():
	stLine = "exec --no-startup-id ~/.fehbg # added by feh-browse"
	if not FileHasLine(I3_CONFIG, stLine):
		AppendFileWithLine(I3_CONFIG, stLine + "\n")

def SetBg():
	arModes = ['scale', 'fill', 'max', 'center', 'tile']
	subprocess.call(['/bin/feh', '--bg-' + arModes[rvMode.get()], DIRECTORY + '/' + svSelectedFile.get()])
	# TO DO: add to favourites list and save in sqlite db - if fails, don't worry about it, just warn

def ScrollHorizontally(event):
	cwFavourites.xview_scroll((event.delta / 120), "units")

def ScrollVertically(event):
	cwPicker.yview_scroll((event.delta / 120), "units")

def ConstrainPickerScroll(event):
	cwPicker.configure(scrollregion=cwPicker.bbox("all"))

def ConstrainRecentScroll(event):
	cwRecent.configure(scrollregion=cwRecent.bbox("all"))

# tags:
# ww - window widget
# fw - frame widget
# rv - radio value
# rw - radio widget
# cw - canvas widget
# sw - scrollbar widget
# bw - button widget
# sv - string value
# ps - pixel size
# sc - scalar value
# ar - array
# fn - filename
# fp - file pointer
# ix - index
# ut - unsanitised text
# st - sanitised text
# lw - label widget
# tw - text widget

# Level 0 widget

wwMain = tkinter.Tk()
wwMain.configure(background=BACKGROUND_COL)
#wwMain.rowconfigure(0, weight=1)
#wwMain.rowconfigure(1, weight=1)
wwMain.rowconfigure(2, weight=3)
wwMain.columnconfigure(0, weight=1) # needed to fill out column

svSelectedFile = tkinter.StringVar() # put current selection filename in here
rvMode = tkinter.IntVar()

# Level 1 widgets

cwPicker = tkinter.Canvas(wwMain, background=BACKGROUND_COL)
cwPicker.grid(row=2, sticky="news")
cwPicker.rowconfigure(0, weight=1)
cwPicker.columnconfigure(0, weight=1)
cwPicker.grid_propagate(False)

cwRecent = tkinter.Canvas(wwMain, background=BACKGROUND_COL, height=150)
cwRecent.grid(row=0, sticky="new")
cwRecent.rowconfigure(0, weight=1)
cwRecent.columnconfigure(0, weight=1)
cwRecent.grid_propagate(False)

cwPicker.update_idletasks()

fwOptions = tkinter.Frame(wwMain, borderwidth=1, relief='sunken', background=BACKGROUND_COL, height=50)
fwOptions.grid(row=1, sticky="ew")
fwOptions.rowconfigure(0, weight=1)
fwOptions.rowconfigure(1, weight=1)
fwOptions.columnconfigure(0, weight=1)
fwOptions.columnconfigure(1, weight=1)
fwOptions.columnconfigure(2, weight=1)
fwOptions.columnconfigure(3, weight=1)
fwOptions.columnconfigure(4, weight=1)
fwOptions.grid_propagate(False)

# Level 2 widgets

fwPicker = tkinter.Frame(cwPicker, borderwidth=1, relief='sunken', background=BACKGROUND_COL)
cwPicker.create_window((0, 0), window=fwPicker, anchor="nw")
fwPicker.rowconfigure(0, weight=1)
fwPicker.columnconfigure(0, weight=1)

swPicker = tkinter.Scrollbar(cwPicker, orient="vertical", command=cwPicker.yview)
swPicker.grid(row=0, column=1, sticky="ns")
cwPicker.configure(yscrollcommand=swPicker.set)
swPicker.columnconfigure(0, weight=1)

fwPicker.bind('<Configure>', ConstrainPickerScroll)

fwRecent = tkinter.Frame(cwRecent, borderwidth=1, relief='sunken', background=BACKGROUND_COL)
cwRecent.create_window((0, 0), window=fwRecent, anchor="nw")
fwRecent.rowconfigure(0, weight=1)
fwRecent.columnconfigure(0, weight=1)

swRecent = tkinter.Scrollbar(cwRecent, orient="horizontal", command=cwRecent.yview)
swRecent.grid(row=1, column=0, sticky="ew")
cwRecent.configure(yscrollcommand=swRecent.set)
swRecent.columnconfigure(0, weight=1)

fwRecent.bind('<Configure>', ConstrainRecentScroll)

rwModeScale = tkinter.Radiobutton(fwOptions, text='Scale', variable=rvMode, value=MODE_SCALE, height=1)
rwModeFill = tkinter.Radiobutton(fwOptions, text='Fill', variable=rvMode, value=MODE_FILL)
rwModeMax = tkinter.Radiobutton(fwOptions, text='Max', variable=rvMode, value=MODE_MAX)
rwModeCentre = tkinter.Radiobutton(fwOptions, text='Centre', variable=rvMode, value=MODE_CENTRE)
rwModeTile = tkinter.Radiobutton(fwOptions, text='Tile', variable=rvMode, value=MODE_TILE)

rwModeScale.configure(background=BACKGROUND_COL)
rwModeFill.configure(background=BACKGROUND_COL)
rwModeMax.configure(background=BACKGROUND_COL)
rwModeCentre.configure(background=BACKGROUND_COL)
rwModeTile.configure(background=BACKGROUND_COL)

rwModeScale.grid(row=0, column=0, sticky="news")
rwModeFill.grid(row=0, column=1, sticky="news")
rwModeMax.grid(row=0, column=2, sticky="news")
rwModeCentre.grid(row=0, column=3, sticky="news")
rwModeTile.grid(row=0, column=4, sticky="news")

bwDoIt = tkinter.Button(fwOptions, text="Set Background", command=SetBg)
bwDoIt.grid(row=1, column=1)

bwQuit = tkinter.Button(fwOptions, text="Close", command=Close)
bwQuit.grid(row=1, column=2)

bwI3Config = tkinter.Button(fwOptions, text="Add to i3", command=WriteI3)
bwI3Config.grid(row=1, column=3)

# Level 3 widgets

UpdatePicker()

wwMain.bind_all('<MouseWheel>', ScrollVertically)
wwMain.bind_all('<Shift-MouseWheel>', ScrollHorizontally)

# TO DO: expand the scrollwheel binding to all widgets not just the scrollbars.

wwMain.mainloop()

