#!/bin/python

import tkinter

MODE_SCALE=1
MODE_FILL=2
MODE_MAX=3
MODE_CENTRE=4
MODE_TILE=5

BACKGROUND_COL='#fdf6e3'

# tags:
# ww - window widget
# fw - frame widget
# rv - radio value
# rw - radio widget
# cw - canvas widget
# sw - scrollbar widget

# Level 0 widget

wwMain = tkinter.Tk()
wwMain.configure(background=BACKGROUND_COL)
wwMain.rowconfigure(0, weight=1) # ??? should be 2?
wwMain.rowconfigure(1, weight=1)
wwMain.rowconfigure(2, weight=1)
wwMain.columnconfigure(0, weight=1) # needed to fill out column

# Level 1 widgets

fwPicker = tkinter.Frame(wwMain, padx=5, pady=5, borderwidth=1, relief='sunken')
fwPicker.grid(row=0, sticky="news")
fwPicker.rowconfigure(0, weight=1)
fwPicker.columnconfigure(0, weight=1)

fwFavourites = tkinter.Frame(wwMain, padx=5, pady=5, borderwidth=1, relief='sunken')
fwFavourites.grid(row=1, sticky="news")
fwFavourites.rowconfigure(0, weight=1)
fwFavourites.columnconfigure(0, weight=1)

fwOptions = tkinter.Frame(wwMain, padx=5, pady=5, borderwidth=1, relief='sunken')
fwOptions.grid(row=2, sticky="news")
fwOptions.rowconfigure(0, weight=1)

# Level 2 widgets

cwPicker = tkinter.Canvas(fwPicker, background='#123456')
cwPicker.grid(row=0, sticky="news")
cwPicker.columnconfigure(0, weight=1)

swPicker = tkinter.Scrollbar(fwPicker, orient="vertical", command=cwPicker.yview)
swPicker.grid(row=0, column=0, sticky="nse")
cwPicker.configure(yscrollcommand=swPicker.set, scrollregion=cwPicker.bbox("all"))
swPicker.columnconfigure(0, weight=1)

cwFavourites = tkinter.Canvas(fwFavourites, background='#654321')
cwFavourites.grid(row=0, sticky="news")
cwFavourites.columnconfigure(0, weight=1)

swFavourites = tkinter.Scrollbar(fwFavourites, orient="horizontal", command=cwFavourites.xview)
swFavourites.grid(row=0, column=0, sticky="ews")
cwFavourites.configure(xscrollcommand=swFavourites.set, scrollregion=cwFavourites.bbox("all"))
swFavourites.rowconfigure(0, weight=1)

#rvMode = tkinter.IntVar()
#rwModeScale = tkinter.Radiobutton(fwOptions, text='Scale', variable=rvMode, value=MODE_SCALE)
#rwModeFill = tkinter.Radiobutton(fwOptions, text='Fill', variable=rvMode, value=MODE_FILL)
#rwModeMax = tkinter.Radiobutton(fwOptions, text='Max', variable=rvMode, value=MODE_MAX)
#rwModeCentre = tkinter.Radiobutton(fwOptions, text='Centre', variable=rvMode, value=MODE_CENTRE)
#rwModeTile = tkinter.Radiobutton(fwOptions, text='Tile', variable=rvMode, value=MODE_TILE)

#rwModeScale.configure(background=BACKGROUND_COL)
#rwModeFill.configure(background=BACKGROUND_COL)
#rwModeMax.configure(background=BACKGROUND_COL)
#rwModeCentre.configure(background=BACKGROUND_COL)
#rwModeTile.configure(background=BACKGROUND_COL)

#rwModeScale.grid(row=0, column=0, sticky="w")
#rwModeFill.grid(row=1, column=0, sticky="w")
#rwModeMax.grid(row=2, column=0, sticky="w")
#rwModeCentre.grid(row=0, column=1, sticky="w")
#rwModeTile.grid(row=1, column=1, sticky="w")

wwMain.mainloop()

