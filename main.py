#!/bin/python

import tkinter
import os
import subprocess
import math
from PIL import Image, ImageTk

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

def Elide(stText, psLength):
	# elide a piece of text so that it's no wider than psLength pixels
	# return the elided text
	if len(stText) > 18:
		stText = stText[0:18] + '...'
	return stText

# redraw on events: resize/reflow, files changed in dir, selection changes
def DrawCanvas():
	cwPicker.delete("ALL")
	cwFavourites.delete("ALL")
	# scan dir, draw canvas items
	if not os.path.exists(DIRECTORY):
		os.makedirs(DIRECTORY, exist_ok=True)
	arFiles = os.listdir(DIRECTORY)
	cwPicker.update_idletasks()
	psCanvas = cwPicker.winfo_width()
	psIconWidth = 150
	psIconHeight = 100
	psTextHeight = 20
	psSpacer = 5
	ixCol = 0
	ixRow = 0
	scIconsPerRow = math.floor(psCanvas / (psIconWidth + psSpacer))
	for fnImage in arFiles:
		# create a thumbnail of fnImage and draw on canvas - process symlinks correctly
		# make clickable :o on click, set svSelectedFile and redraw
		imThumb = None
		try:
			imThumb = Image.open(DIRECTORY + '/' + fnImage)
			imThumb.thumbnail((psIconWidth - (2 * psSpacer), psIconHeight - psTextHeight), Image.ANTIALIAS)
			imTkThumb = ImageTk.PhotoImage(imThumb)
			cwPicker.create_image(ixCol * psIconWidth + psSpacer, ixRow * psIconHeight, image=imTkThumb)
		except:
			cwPicker.create_rectangle(ixCol * psIconWidth + psSpacer, ixRow * psIconHeight, (ixCol + 1) * psIconWidth - psSpacer, (ixRow + 1) * psIconHeight - psTextHeight, fill='blue')
		# show trimmed down filename
		stTrimmed = Elide(SanitiseFilename(fnImage), psIconWidth - (2 * psSpacer))
		cwPicker.create_text((ixCol + 0.5) * psIconWidth, (ixRow + 1) * psIconHeight - (psTextHeight * 0.5), text=stTrimmed)
		# if selected, draw a border on it
		if fnImage == svSelectedFile.get():
			cwPicker.create_line(ixCol * psIconWidth, ixRow * psIconHeight, ixCol * psIconWidth, (ixRow + 1) * psIconHeight, fill="red")
			cwPicker.create_line((ixCol + 1) * psIconWidth, ixRow * psIconHeight, (ixCol + 1) * psIconWidth, (ixRow + 1) * psIconHeight, fill="red")
		ixCol = ixCol + 1
		ixCol = ixCol % scIconsPerRow 
		if ixCol == 0:
			ixRow = ixRow + 1

	# also on favourites (recent ones in sequence) - read sqlite db
	# ...?
	# re-constrain scrollbars
	cwPicker.configure(scrollregion=cwPicker.bbox("all"))
	cwFavourites.configure(scrollregion=cwFavourites.bbox("all"))

def Close():
	wwMain.destroy()

def WriteI3():
	# Write "exec --no-startup-id ~/.fehbg" to the file .config/i3/config
	with open(I3_CONFIG, "a") as config:
		config.write('# added by feh-browse\n')
		config.write('exec --no-startup-id ~/.fehbg\n\n')

def SetBg():
	arModes = ['scale', 'fill', 'max', 'center', 'tile']
	subprocess.call(['/bin/feh', '--bg-' + arModes[rvMode.get()], DIRECTORY + '/' + svSelectedFile.get()])
	# TO DO: add to favourites list and save in sqlite db - if fails, don't worry about it, just warn

def ScrollHorizontally(event):
	cwFavourites.yview_scroll((event.delta / 120), "units")

def ScrollVertically(event):
	cwPicker.xview_scroll((event.delta / 120), "units")

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
# ix - index
# ut - unsanitised text
# st - sanitised text

# Level 0 widget

wwMain = tkinter.Tk()
wwMain.configure(background=BACKGROUND_COL)
wwMain.rowconfigure(0, weight=1) # ??? should be 2?
wwMain.rowconfigure(1, weight=1)
wwMain.rowconfigure(2, weight=1)
wwMain.columnconfigure(0, weight=1) # needed to fill out column

# Level 1 widgets

fwPicker = tkinter.Frame(wwMain, padx=5, pady=5, borderwidth=1, relief='sunken', background=BACKGROUND_COL)
fwPicker.grid(row=0, sticky="news")
fwPicker.rowconfigure(0, weight=1)
fwPicker.columnconfigure(0, weight=1)

fwFavourites = tkinter.Frame(wwMain, padx=5, pady=5, borderwidth=1, relief='sunken', background=BACKGROUND_COL)
fwFavourites.grid(row=1, sticky="news")
fwFavourites.rowconfigure(0, weight=1)
fwFavourites.columnconfigure(0, weight=1)

fwOptions = tkinter.Frame(wwMain, padx=5, pady=5, borderwidth=1, relief='sunken', background=BACKGROUND_COL)
fwOptions.grid(row=2, sticky="news")
fwOptions.rowconfigure(0, weight=1)
fwOptions.rowconfigure(1, weight=1)
fwOptions.rowconfigure(2, weight=1)
fwOptions.rowconfigure(3, weight=1)

# Level 2 widgets

cwPicker = tkinter.Canvas(fwPicker, background=BACKGROUND_COL)
cwPicker.grid(row=0, sticky="news")
cwPicker.columnconfigure(0, weight=1)

swPicker = tkinter.Scrollbar(fwPicker, orient="vertical", command=cwPicker.yview)
swPicker.grid(row=0, column=0, sticky="nse")
cwPicker.configure(yscrollcommand=swPicker.set, scrollregion=cwPicker.bbox("all"))
swPicker.columnconfigure(0, weight=1)

cwFavourites = tkinter.Canvas(fwFavourites, height="0", background=BACKGROUND_COL)
cwFavourites.grid(row=0, sticky="news")
cwFavourites.columnconfigure(0, weight=1)

swFavourites = tkinter.Scrollbar(fwFavourites, orient="horizontal", command=cwFavourites.xview)
swFavourites.grid(row=0, column=0, sticky="ews")
cwFavourites.configure(xscrollcommand=swFavourites.set, scrollregion=cwFavourites.bbox("all"))
swFavourites.rowconfigure(0, weight=1)

svSelectedFile = tkinter.StringVar() # put current selection filename in here

rvMode = tkinter.IntVar()
rwModeScale = tkinter.Radiobutton(fwOptions, text='Scale', variable=rvMode, value=MODE_SCALE)
rwModeFill = tkinter.Radiobutton(fwOptions, text='Fill', variable=rvMode, value=MODE_FILL)
rwModeMax = tkinter.Radiobutton(fwOptions, text='Max', variable=rvMode, value=MODE_MAX)
rwModeCentre = tkinter.Radiobutton(fwOptions, text='Centre', variable=rvMode, value=MODE_CENTRE)
rwModeTile = tkinter.Radiobutton(fwOptions, text='Tile', variable=rvMode, value=MODE_TILE)

rwModeScale.configure(background=BACKGROUND_COL)
rwModeFill.configure(background=BACKGROUND_COL)
rwModeMax.configure(background=BACKGROUND_COL)
rwModeCentre.configure(background=BACKGROUND_COL)
rwModeTile.configure(background=BACKGROUND_COL)

rwModeScale.grid(row=0, column=0, sticky="w")
rwModeFill.grid(row=1, column=0, sticky="w")
rwModeMax.grid(row=2, column=0, sticky="w")
rwModeCentre.grid(row=0, column=1, sticky="w")
rwModeTile.grid(row=1, column=1, sticky="w")

bwDoIt = tkinter.Button(fwOptions, text="Set Background", command=SetBg)
bwDoIt.grid(row=3, column=1)

bwQuit = tkinter.Button(fwOptions, text="Close", command=Close)
bwQuit.grid(row=3, column=3)

bwI3Config = tkinter.Button(fwOptions, text="Add to i3", command=WriteI3)
bwI3Config.grid(row=3, column=2)

DrawCanvas()

wwMain.bind_all('<MouseWheel>', ScrollVertically)
wwMain.bind_all('<Shift-MouseWheel>', ScrollHorizontally)

# TO DO: expand the scrollwheel binding to all widgets not just the scrollbars.

wwMain.mainloop()

