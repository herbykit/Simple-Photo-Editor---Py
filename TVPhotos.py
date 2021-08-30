#! Just starting out the program to be executable
from PIL import Image, ImageOps, ImageDraw, ImageFont
import wx
import os.path
import shutil
import time
import math

window = wx.App(False);
directory = ""
chosen = False
global fileNameHolder, currentImage, amount, container, x, y
amount = 0
currentImage = wx.EmptyImage(1,1)
container = wx.Frame(None, wx.ID_ANY, "Picture Editing")
container.Maximize()
left = wx.Panel(container, wx.ID_ANY)
right = wx.Panel(container, wx.ID_ANY)
bothSidesContainer = wx.BoxSizer(wx.HORIZONTAL)
bothSidesContainer.Add(left, 1, wx.ALIGN_LEFT | wx.EXPAND)
bothSidesContainer.Add(right, 3, wx.ALIGN_RIGHT | wx.EXPAND)
leftOrganiser = wx.BoxSizer(wx.VERTICAL)
rightOrganiser = wx.BoxSizer(wx.HORIZONTAL)
sizeToFill = container.GetSize()
x = sizeToFill[0]
y = sizeToFill[1]

## Directory selection button
chooseDirectory = wx.Button(left, wx.ID_ANY, label="Choose Directory:")
# The chosen directory displayed as StaticText to the right of the button
selection = wx.StaticText(left)
# Sizer to keep these two aligned properly lol
anotherSizer = wx.BoxSizer(wx.HORIZONTAL)
anotherSizer.Add(chooseDirectory, 1, wx.SHAPED)
anotherSizer.Add(selection, 2, wx.SHAPED)

rename = wx.StaticText(left, wx.ID_ANY, "Rename file here:  ")

fileNameHolder = wx.TextCtrl(left, wx.ID_ANY, "File name")
midSection = wx.BoxSizer(wx.HORIZONTAL)
midSection.Add(rename, 1, wx.EXPAND)
midSection.Add(fileNameHolder, 2, wx.EXPAND)

resizing = wx.Button(left, wx.ID_ANY, label="Resize image to window")
resizer = wx.BoxSizer(wx.HORIZONTAL)
resizer.Add(resizing, 1, wx.EXPAND)

row = wx.GridSizer(rows=1, cols=4, hgap=4, vgap=4)
for button in ["90", "180", "Offset <", "Offset >"]:
	thing = wx.Button(left, wx.ID_ANY, label=button)
	def rotate(event, GIMMEDANAME=button):
		rotation(GIMMEDANAME)
	thing.Bind(wx.EVT_BUTTON, rotate)
	row.Add(thing, 1, wx.SHAPED)

## This is where to add the caption thing and add it to left sizer
submission = wx.Button(left, wx.ID_ANY, label="Submit")
last = wx.BoxSizer(wx.HORIZONTAL)
last.Add(submission, 4, wx.EXPAND)

def replaceWithImage(image):
	global right, x, y
	## Get the previous image
	if right.GetChildren():
		for selectedFile in right.GetChildren():
			## Remove the previous image
			selectedFile.Destroy()

	## Add the next image
	global editer
	editer = Image.open(image)
	editer.thumbnail((x,y))

	global showImage
	showImage = wx.Image(image)
	shower = wx.StaticBitmap(right, wx.ID_ANY, wx.BitmapFromImage(showImage))
	rightOrganiser.Add(shower, 1, wx.ALIGN_CENTER | wx.EXPAND)

def pattern(directory):
	x = 0
	y = len(os.listdir(directory))
	print(y)
	for img in os.listdir(directory):
		x = x + 1
		if (img.endswith(".jpg") or img.endswith(".JPG")):
			if not os.path.exists(directory+"\\Edited Photos"):
				os.mkdir(directory+"\\Edited Photos")
				print("Made Edited Photos directory!")
			if not os.path.exists(directory+"\\Original Photos"):
				os.mkdir(directory+"\\Original Photos")
				print("Made Original Photos directory!")
			global amount, currentImage
			amount = 0
			currentImage = directory+"//"+img
			## Reset text in fileNameHolder each time
			fileNameHolder.SetLabel(os.path.splitext(img)[0]) ## New line
			replaceWithImage(currentImage)
			break
		elif not (img.endswith(".JPG") or img.endswith(".jpg")) and y == x:
			print("No more pictures in this directory")
			exit()
def saveImage(asname):
	global editer, currentImage
	editer.save(os.path.dirname(currentImage)+"//Edited Photos//"+asname+"TV.JPG")
	shutil.move(currentImage, os.path.dirname(currentImage)+"//Original Photos//"+asname+".JPG")
	if os.path.exists(currentImage):
		print("No more picture files in directory")
		exit()

def dirClicked(event):
	dia = wx.DirDialog(container, "Choose the parent directory", "C:/", 0, (10,10), wx.Size(400,300))
    	dun = dia.ShowModal()
    	if dun == wx.ID_OK:
        	directory = dia.GetPath()
        	selection.SetLabel(directory)
        	pattern(directory)
        	return directory
    	elif dun != wx.ID_OK:
    		directory = ""
    		return directory

def rotation(direction):
	global showImage, amount, editer, x, y, right
	d = right.GetChildren()
	editer.thumbnail((x,y))
	if direction=="90":
		editer = editer.transpose(Image.ROTATE_90)
		showImage = wx.EmptyImage(editer.size[0],editer.size[1])
		showImage.SetData(editer.convert('RGB').tostring())
		for selectedFile in d:
			NEXT = wx.StaticBitmap(right, wx.ID_ANY, wx.BitmapFromImage(showImage))
			selectedFile.Destroy()
		rightOrganiser.Add(NEXT, 1, wx.ALIGN_CENTER | wx.EXPAND)
	elif direction=="180":
		amount = amount+.001
		editer = editer.transpose(Image.ROTATE_180)
		showImage = wx.EmptyImage(editer.size[0],editer.size[1])
		showImage.SetData(editer.convert('RGB').tostring())
		for selectedFile in d:
			NEXT = wx.StaticBitmap(right, wx.ID_ANY, wx.BitmapFromImage(showImage))
			selectedFile.Destroy()
		rightOrganiser.Add(NEXT, 1, wx.ALIGN_CENTER | wx.EXPAND)

def getName():
	global fileNameHolder
	TOOMUCH = fileNameHolder.GetValue()
	return TOOMUCH

def resizeIt(stupidevent):
	global editer, x, y, showImage
	d = right.GetChildren()
	editer.thumbnail((x, y))
	showImage = wx.EmptyImage(editer.size[0],editer.size[1])
	showImage.SetData(editer.convert('RGB').tostring())
	for selectedFile in d:
		selectedFile.Destroy()
	NEXT = wx.StaticBitmap(right, wx.ID_ANY, wx.BitmapFromImage(showImage))
	rightOrganiser.Add(NEXT, 1, wx.ALIGN_CENTER | wx.EXPAND)

## Allow editing for font and color to be seen best. BLACK OR WHITE
# Text Input
capterr = wx.StaticText(left, wx.ID_ANY, "Input caption here:")
capter = wx.TextCtrl(left, wx.ID_ANY, "")
caption1 = wx.BoxSizer(wx.HORIZONTAL)
caption2 = wx.BoxSizer(wx.HORIZONTAL)
caption1.Add(capterr)
caption1.Add(capter)
global newedit
# Text Shown consistently, when button is pressed
for nummy in ["Black","White"]:
	tinktink = wx.Button(left,wx.ID_ANY,label=nummy)
	caption2.Add(tinktink)
	def addText(name=tinktink):
		global editer
		global showImage
		if name == "White":
			color=(255,255,255)
		elif name == "Black":
			color=(0,0,0)
		newedit = ImageDraw.Draw(editer)
		newedit.text((0,editer.size[1]),text=capter.GetValue(),font=ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf',18),fill=color)
		nexter = wx.EmptyImage(editor.size[0],editer.size[1])
		nexter.SetData(newedit.convert('RGB').tostring())
		for lalala in right.GetChildren():
			lalala.Destroy()
		rightOrganiser.Add(nexter, 1, wx.ALIGN_CENTER | wx.EXPAND)
	tinktink.Bind(wx.EVT_BUTTON, addText)

def submitting(takeit):
	global currentImage
	saveImage(getName())
	pattern(os.path.dirname(currentImage))

left.Bind(wx.EVT_BUTTON, submitting, submission)
resizing.Bind(wx.EVT_BUTTON, resizeIt)
left.Bind(wx.EVT_BUTTON, dirClicked, chooseDirectory)
leftOrganiser.Add(anotherSizer)
leftOrganiser.Add(midSection)
leftOrganiser.Add(row)
leftOrganiser.Add(resizer)
leftOrganiser.Add(caption1)
leftOrganiser.Add(caption2)
leftOrganiser.Add(last)
## Show the GUI
right.SetSizer(rightOrganiser)
left.SetSizer(leftOrganiser)
container.SetSizer(bothSidesContainer)
container.SetAutoLayout(1)
bothSidesContainer.Fit(container)
container.Show(True)

dirClicked("a")

window.MainLoop()
exit()