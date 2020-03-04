from .stderr import eprint 

import tkinter
import os

# pixbuf
import gi
gi.require_version('GdkPixbuf', '2.0')
from gi.repository.GdkPixbuf import Pixbuf, InterpType

from PIL import ImageTk

DIR_THUMBS=os.path.expanduser('~/.thumbs')

if not os.path.isdir(DIR_THUMBS):
	# create .thumbs dir if absent, 0700 preferred
	os.mkdir(DIR_THUMBS, 0o700)

# tags:
# pb - pixbuf image
# dn - dir name

# TO DO: deal with this error: ie. faulty image file, don't want crash
#Traceback (most recent call last):
#  File "./main.py", line 289, in <module>
#    UpdatePicker()
#  File "./main.py", line 102, in UpdatePicker
#    pbThumb = Pixbuf.new_from_file(DIRECTORY + '/' + fnImage)
#gi.repository.GLib.Error: gdk-pixbuf-error-quark: Image file “/home/DREAMTRACK.CO.UK/w131032/Wallpaper/temp.0” contains no data (0)

class IconTile:
	'icon tile class'
	dnImages = ''
	fnImage = ''
	psWidth = 150
	psHeight = 100
	def __init__(self, dnImages = '', fnImage = '', psWidth = 150, psHeight = 100):
		self.dnImages = dnImages
		self.fnImage = fnImage
		self.psWidth = psWidth
		self.psHeight = psHeight
	def draw(self, lwIcon = None):
		# check thumbnail exists
		pbThumb = None
		fnThumb = DIR_THUMBS + '/' + self.fnImage + '.png'
		if not os.path.isfile(fnThumb):
			# create thumbnail
			pbThumb = Pixbuf.new_from_file(self.dnImages + '/' + self.fnImage)
			pbThumb = pbThumb.scale_simple(self.psWidth, self.psHeight, InterpType.NEAREST)
			pbThumb.savev(fnThumb, 'png', [], [])
		# load thumbnail
		imTkThumb = ImageTk.PhotoImage(file=fnThumb)
		lwIcon.configure(image=imTkThumb)
		lwIcon.image = imTkThumb # apparently PIL has a reference counting bug which causes the image to be garbage collected before it's used? See comment in https://github.com/NabaSadiaSiddiqui/Mausam/blob/master/Entry.py, line 110

