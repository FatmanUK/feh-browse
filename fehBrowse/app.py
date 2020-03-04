# 0000000111111111122222222223333333333444444444455555555556666666666777
# 3456789012345678901234567890123456789012345678901234567890123456789012

# TO DO: test with JPG, PNG, GIF, BMP, TIF image types

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
# dr - db row

import os
import math
import subprocess
import sqlite3

from tkinter import Tk, IntVar, StringVar, Canvas, Frame, Scrollbar
from tkinter import Button, Radiobutton, Label
from .stderr import eprint
from .icontile import IconTile

# app constants
TITLE="feh-browse"
MODE_SCALE=0
MODE_FILL=1
MODE_MAX=2
MODE_CENTRE=3
MODE_TILE=4
HIGHLIGHT_COL='#ff6600'
DIRECTORY=os.path.expanduser('~/Wallpaper')
I3_CONFIG=os.path.expanduser('~/.config/i3/config')
DB_PATH=os.path.expanduser('~/.feh-browse.sqlite')

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

def DeleteAllWidgetsIn(fwFrame):
	for w in fwFrame.winfo_children():
		w.destroy()

class fehBrowse:
	wwUi = Tk()
	rvMode = IntVar()
	svPicked = StringVar()
	psIconWidth = 150
	psIconHeight = 100
	psBorder = 4
	psSpacing = 5
	def __init__(self):
		self.MakeWidgets()
	def UpdatePicker(self):
		cwPicker = self.GetPicker()
		fwPicker = cwPicker.nametowidget("fwPicker")
		cwPicker.update_idletasks()
		fwPicker.update_idletasks()
		DeleteAllWidgetsIn(fwPicker)
		# set loop variables
		psCanvasWidth = cwPicker.winfo_width()
		psTextHeight = 20
		scIconsPerRow = math.floor(	psCanvasWidth
						/ (self.psIconWidth
						+ (2 * self.psBorder)))
		ixCol = 0
		ixRow = 0
		# scan directory
		if not os.path.exists(DIRECTORY):
			os.makedirs(DIRECTORY, exist_ok=True)
		arFiles = sorted(os.listdir(DIRECTORY))
		for fnImage in arFiles:
			fwHilit = self.CreateHighlight(	fwPicker,
							fnImage,
							ixRow, ixCol)
			self.CreateSpacer(fwPicker, ixRow, ixCol)
			self.CreateOutput(	fnImage, fwHilit, ixRow,
						ixCol)
			ixCol = ixCol + 1
			ixCol = ixCol % scIconsPerRow
			if ixCol == 0:
				ixRow = ixRow + 1
	def UpdateRecent(self):
		cwRecent = self.GetRecent()
		fwRecent = cwRecent.nametowidget("fwRecent")
		cwRecent.update_idletasks()
		fwRecent.update_idletasks()
		DeleteAllWidgetsIn(fwRecent)
		arFiles = []
		try:
			conn = sqlite3.connect(DB_PATH)
			curs = conn.cursor()
			q = 'SELECT file FROM recents ORDER BY id DESC;'
			arResults = curs.execute(q)
			for drRow in arResults:
				arFiles.append(drRow[0])
			conn.close()
		except:
			m = 'Database operations failed. Check file '
			m = m + 'permissions on %s?' % DB_PATH
			eprint(m)
		ixCol = 0
		for fnImage in arFiles:
			fwHilit = self.CreateHighlight(	fwRecent,
							fnImage,
							0, ixCol)
			self.CreateSpacer(fwRecent, 0, ixCol)
			self.CreateOutput(fnImage, fwHilit, 0, ixCol)
			ixCol = ixCol + 1
	def ClickedIcon(self, fnImage):
		self.svPicked.set(fnImage)
		self.UpdatePicker()
	def ConstrainPickerScroll(self, event=None):
		cwPicker = self.GetPicker()
		cwPicker.configure(scrollregion=cwPicker.bbox("all"))
	def ConstrainRecentScroll(self, event=None):
		cwRecent = self.GetRecent()
		cwRecent.configure(scrollregion=cwRecent.bbox("all"))
	def ScrollHorizontally(self, event):
		self.GetRecent().xview_scroll(	(event.delta / 120),
						"units")
	def ScrollVertically(self, event):
		self.GetRecent().yview_scroll(	(event.delta / 120),
						"units")
	def SetBg(self):
		arModes = ['scale', 'fill', 'max', 'center', 'tile']
		arCmd = [	'/bin/feh',
				'--bg-' + arModes[self.rvMode.get()],
				DIRECTORY + '/' + self.svPicked.get() ]
		subprocess.call(arCmd)
		try:
			arFile = (self.svPicked.get(),)
			conn = sqlite3.connect(DB_PATH)
			curs = conn.cursor()
			q = 'CREATE TABLE IF NOT EXISTS recents (id'
			q = q + ' INTEGER PRIMARY KEY AUTOINCREMENT,'
			q = q + ' file VARCHAR(1024));'
			curs.execute(q)
			q = 'DELETE FROM recents WHERE file=?;'
			curs.execute(q, arFile)
			q = 'INSERT INTO recents (file) VALUES (?);'
			curs.execute(q, arFile)
			conn.commit()
			conn.close()
		except:
			m = 'Database operations failed. Check file '
			m = m + 'permissions on %s?' % DB_PATH
			eprint(m)
		self.UpdateRecent()
	def Close(self):
		self.wwUi.destroy()
	def CreateHighlight(self, fwParent, fnImage, ixRow, ixCol):
		psWidth = self.psIconWidth + (2 * self.psBorder)
		psHeight = self.psIconHeight + (2 * self.psBorder)
		fwHilit = Frame(fwParent, borderwidth=0, width=psWidth,
				height=psHeight)
		if fnImage == self.svPicked.get():
			fwHilit.configure(background=HIGHLIGHT_COL)
		fwHilit.grid(row=(ixRow * 3), column=(ixCol * 2))
		fwHilit.bind(	"<Button-1>",
				lambda event,
				a=fnImage:self.ClickedIcon(a))
		return fwHilit
	def CreateSpacer(self, fwParent, ixRow, ixCol):
		fwSpacer = Frame(	fwParent, borderwidth=0,
					width=self.psSpacing,
					height=self.psSpacing)
		fwSpacer.grid(	row=(ixRow * 3) + 2,
				column=(ixCol * 2) + 1)
	def CreateOutput(self, fnImage, fwHilit, ixRow, ixCol):
		i = IconTile(	DIRECTORY, fnImage, self.psIconWidth,
				self.psIconHeight)
		lwIcon = Label(fwHilit)
		lwIcon.bind(	"<Button-1>",
				lambda event,
				a=fnImage:self.ClickedIcon(a))
		# slightly dodgy using place within grid :/
		lwIcon.place(relx=0.5, rely=0.5, anchor="center")
		i.draw(lwIcon)
	def MakePicker(self):
		cwPicker = Canvas(self.wwUi, name='cwPicker')
		cwPicker.grid(row=2, sticky="news")
		cwPicker.rowconfigure(0, weight=1)
		cwPicker.columnconfigure(0, weight=1)
		cwPicker.grid_propagate(False)
		return cwPicker
	def GetPicker(self):
		return self.wwUi.nametowidget('cwPicker')
	def MakeRecent(self):
		cwRecent = Canvas(	self.wwUi, name='cwRecent',
					height=150)
		cwRecent.grid(row=0, sticky="new")
		cwRecent.rowconfigure(0, weight=1)
		cwRecent.columnconfigure(0, weight=1)
		cwRecent.grid_propagate(False)
		return cwRecent
	def GetRecent(self):
		return self.wwUi.nametowidget('cwRecent')
	def MakeButtonPanel(self):
		fwOptions = Frame(	self.wwUi, borderwidth=1,
					relief='sunken', height=50,
					name='fwOptions')
		fwOptions.grid(row=1, sticky="ew")
		fwOptions.rowconfigure(0, weight=1)
		fwOptions.rowconfigure(1, weight=1)
		fwOptions.columnconfigure(0, weight=1)
		fwOptions.columnconfigure(1, weight=1)
		fwOptions.columnconfigure(2, weight=1)
		fwOptions.columnconfigure(3, weight=1)
		fwOptions.columnconfigure(4, weight=1)
		fwOptions.grid_propagate(False)
		return fwOptions
	def GetButtonPanel(self):
		return self.wwUi.nametowidget('fwOptions')
	def MakeWidgets(self):
		self.wwUi.title(TITLE)
		self.wwUi.rowconfigure(2, weight=3)
		# needed to fill out column
		self.wwUi.columnconfigure(0, weight=1)
		cwPicker = self.MakePicker()
		cwRecent = self.MakeRecent()
		# can't remember why
		self.GetPicker().update_idletasks()
		fwOptions = self.MakeButtonPanel()
		# next level of widgets
		fwPicker = Frame(	cwPicker, borderwidth=0,
					relief='sunken',
					name='fwPicker')
		cwPicker.create_window(	(0, 0), window=fwPicker,
					anchor="nw")
		fwPicker.rowconfigure(0, weight=1)
		fwPicker.columnconfigure(0, weight=1)
		swPicker = Scrollbar(	cwPicker, orient="vertical",
					command=cwPicker.yview)
		swPicker.grid(row=0, column=1, sticky="ns")
		cwPicker.configure(yscrollcommand=swPicker.set)
		swPicker.columnconfigure(0, weight=1)
		fwPicker.bind('<Configure>', self.ConstrainPickerScroll)
		fwRecent = Frame(	cwRecent, borderwidth=1,
					relief='sunken',
					name='fwRecent')
		cwRecent.create_window(	(0, 0), window=fwRecent,
					anchor="nw")
		fwRecent.rowconfigure(0, weight=1)
		fwRecent.columnconfigure(0, weight=1)
		swRecent = Scrollbar(	cwRecent, orient="horizontal",
					command=cwRecent.yview)
		swRecent.grid(row=1, column=0, sticky="ew")
		cwRecent.configure(yscrollcommand=swRecent.set)
		swRecent.columnconfigure(0, weight=1)
		fwRecent.bind('<Configure>', self.ConstrainRecentScroll)
		rwModeScale = Radiobutton(	fwOptions, text='Scale',
						variable=self.rvMode,
						value=MODE_SCALE,
						height=1)
		rwModeFill = Radiobutton(	fwOptions, text='Fill',
						variable=self.rvMode,
						value=MODE_FILL)
		rwModeMax = Radiobutton(fwOptions, text='Max',
					variable=self.rvMode,
					value=MODE_MAX)
		rwModeCentre = Radiobutton(	fwOptions,
						text='Centre',
						variable=self.rvMode,
						value=MODE_CENTRE)
		rwModeTile = Radiobutton(	fwOptions, text='Tile',
						variable=self.rvMode,
						value=MODE_TILE)
		rwModeScale.grid(row=0, column=0, sticky="news")
		rwModeFill.grid(row=0, column=1, sticky="news")
		rwModeMax.grid(row=0, column=2, sticky="news")
		rwModeCentre.grid(row=0, column=3, sticky="news")
		rwModeTile.grid(row=0, column=4, sticky="news")
		bwDoIt = Button(fwOptions, text="Set Background",
				command=self.SetBg)
		bwDoIt.grid(row=1, column=1)
		bwQuit = Button(fwOptions, text="Close",
				command=self.Close)
		bwQuit.grid(row=1, column=2)
		bwI3Config = Button(	fwOptions, text="Add to i3",
					command=WriteI3)
		bwI3Config.grid(row=1, column=3)
		self.UpdatePicker()
		self.UpdateRecent()
		# TO DO: expand the scrollwheel binding to all widgets
		# not just the scrollbars.
		self.wwUi.bind_all(	'<MouseWheel>',
					self.ScrollVertically)
		self.wwUi.bind_all(	'<Shift-MouseWheel>',
					self.ScrollHorizontally)
		# TO DO: make resize-redraw work without crashing
		#self.wwUi.bind('<Configure>', ResizeWindow)
		self.wwUi.mainloop()
	@staticmethod
	def run(arArgs):
		this = fehBrowse()

