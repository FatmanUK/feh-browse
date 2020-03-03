#!/bin/python

from stderr import *
from icontile import *

import math
import subprocess

TITLE="feh-browse"

MODE_SCALE=0
MODE_FILL=1
MODE_MAX=2
MODE_CENTRE=3
MODE_TILE=4

BACKGROUND_COL='#dddddd'
HIGHLIGHT_COL='#ff0000'

DIRECTORY=os.path.expanduser('~/Wallpaper')
I3_CONFIG=os.path.expanduser('~/.config/i3/config')

# BUGS:
# 2: (blocks alpha) redraw picker and recents on window resize
# 3: (blocks beta)  sanitise the filename properly
# 4: (blocks beta)  proper elide function
# 5: (blocks alpha) recents frame and UpdateRecents function
# 6: (blocks alpha) actual recents update using SQLite database
# 7: (blocks beta)  make scrollbars work properly on all windows. Something about focus?

def SanitiseFilename(utText):
	# TO DO: sanitise a filename and return a good version
	return utText

def Elide(stText, psLength = 0):
	# elide a piece of text so that it's no wider than psLength pixels
	# return the elided text
	MAXLEN=25
	if len(stText) > MAXLEN:
		stText = stText[0:MAXLEN] + '...'
	return stText

def ClickedIcon(fnImage):
	svSelectedFile.set(fnImage)
#	eprint('Selected: ' + svSelectedFile.get() + '!')
	UpdatePicker()

def UpdateRecent():
	# TO DO: this
	x=1

def DeleteAllWidgetsIn(fwFrame):
	for w in fwFrame.winfo_children():
		w.destroy()

def CreateHighlightFrame(fwPicker, fnImage, psIconWidth, psIconHeight, ixRow, ixCol):
	if fnImage == svSelectedFile.get():
		fwHilit = tkinter.Frame(fwPicker, borderwidth=0, background=HIGHLIGHT_COL, width=psIconWidth, height=psIconHeight)
	else:
		fwHilit = tkinter.Frame(fwPicker, borderwidth=0, background=BACKGROUND_COL, width=psIconWidth, height=psIconHeight)
	fwHilit.grid(row=(ixRow * 3), column=(ixCol * 2))
	fwHilit.bind("<Button-1>", lambda event, a=fnImage:ClickedIcon(a))
	return fwHilit

def CreateSpacer(fwPicker, ixRow, ixCol):
	psPadWidth = 5
	psPadHeight = 5
	fwSpacer = tkinter.Frame(fwPicker, borderwidth=0, background=BACKGROUND_COL, width=psPadWidth, height=psPadHeight)
	fwSpacer.grid(row=(ixRow * 3) + 2, column=(ixCol * 2) + 1)

def CreateOutput(fnImage, psIconWidth, psIconHeight, fwHilit, ixRow, ixCol):
	psHighlightWidth = 10
	psHighlightHeight = 10
	stName = Elide(SanitiseFilename(fnImage))
	i = IconTile(DIRECTORY, fnImage, psIconWidth - (2 * psHighlightWidth), psIconHeight - (2 * psHighlightHeight))
	lwIcon = tkinter.Label(fwHilit)
	lwIcon.bind("<Button-1>", lambda event, a=fnImage:ClickedIcon(a))
	# slightly dodgy using place within grid I know, but it works :)
	lwIcon.place(relx=0.5, rely=0.5, anchor="center")
	try:
		i.draw(lwIcon)
	except OSError:
		stName = "Unknown file type!"
	except:
		x=1
	# TO DO: tooltip with full name? Remove text label then?
	# add label widget
	lwName = tkinter.Label(fwPicker, text=stName)
	lwName.grid(row=(ixRow * 3) + 1, column=(ixCol * 2))


def UpdatePicker():
	cwPicker.update_idletasks()
	fwPicker.update_idletasks()
	DeleteAllWidgetsIn(fwPicker)
	# set loop variables
	psCanvasWidth = cwPicker.winfo_width()
	psIconWidth = 170 # total width including highlight
	psIconHeight = 120 # total height including highlight (but not text)
	psTextHeight = 20
	scIconsPerRow = math.floor(psCanvasWidth / psIconWidth)
	ixCol = 0
	ixRow = 0
	# scan directory
	if not os.path.exists(DIRECTORY):
		os.makedirs(DIRECTORY, exist_ok=True)
	arFiles = sorted(os.listdir(DIRECTORY))
	for fnImage in arFiles:
		fwHilit = CreateHighlightFrame(fwPicker, fnImage, psIconWidth, psIconHeight, ixRow, ixCol)
		CreateSpacer(fwPicker, ixRow, ixCol)
		CreateOutput(fnImage, psIconWidth, psIconHeight, fwHilit, ixRow, ixCol)
		ixCol = ixCol + 1
		ixCol = ixCol % scIconsPerRow
		if ixCol == 0:
			ixRow = ixRow + 1

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
	# TO DO: add to recents list and save in sqlite db - if fails, don't worry about it, just warn
	# TO DO: add to recents frame, database and update recents

def ScrollHorizontally(event):
	cwFavourites.xview_scroll((event.delta / 120), "units")

def ScrollVertically(event):
	cwPicker.yview_scroll((event.delta / 120), "units")

def ResizeWindow(event):
	# TO DO: work out how to resize without crashing
	eprint("resize")

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
wwMain.title(TITLE)
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

fwPicker = tkinter.Frame(cwPicker, borderwidth=0, relief='sunken', background=BACKGROUND_COL)
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

#wwMain.bind_all('<MouseWheel>', ScrollVertically)
#wwMain.bind_all('<Shift-MouseWheel>', ScrollHorizontally)

# TO DO: expand the scrollwheel binding to all widgets not just the scrollbars.

wwMain.bind('<Configure>', ResizeWindow)

wwMain.mainloop()

