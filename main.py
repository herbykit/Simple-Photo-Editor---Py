#! Just starting out the program to be executable
from PIL import Image, ImageOps, ImageDraw, ImageFont
import photo_functions as functions
import file_name_pattern
import wx
import os.path
import shutil
import time
import math

# Defining variables referenced in functions that are stored outside the function
global file_name_holder
# Defining some variables used in the UI within some functions
global right, xSize, ySize


##### Building the GUI #####
window = wx.App(False);
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
xSize = sizeToFill[0]
ySize = sizeToFill[1]

## Directory selection button
chooseDirectory = wx.Button(left, wx.ID_ANY, label="Choose Directory:")
# The chosen directory displayed as StaticText to the right of the button
selection = wx.StaticText(left)
# Sizer to keep these two aligned properly
anotherSizer = wx.BoxSizer(wx.HORIZONTAL)
anotherSizer.Add(chooseDirectory, 1, wx.SHAPED)
anotherSizer.Add(selection, 2, wx.SHAPED)

# A textbox area for the ability to type in a new name for the file
rename = wx.StaticText(left, wx.ID_ANY, "Rename file here:  ")
fileNameHolder = wx.TextCtrl(left, wx.ID_ANY, "File name")
midSection = wx.BoxSizer(wx.HORIZONTAL)
midSection.Add(rename, 1, wx.EXPAND)
midSection.Add(fileNameHolder, 2, wx.EXPAND)

# A section for resizing the image properly
resizing = wx.Button(left, wx.ID_ANY, label="Resize image to window")
resizer = wx.BoxSizer(wx.HORIZONTAL)
resizer.Add(resizing, 1, wx.EXPAND)

# A grid of 4 horizontal buttons to choose what each button does
row = wx.GridSizer(rows=1, cols=4, hgap=4, vgap=4)
for button in ["90", "180", "Offset <", "Offset >"]:
	thing = wx.Button(left, wx.ID_ANY, label=button)
	def rotate(event, name=button):
		functions.rotation(name)
	thing.Bind(wx.EVT_BUTTON, rotate)
	row.Add(thing, 1, wx.SHAPED)

## This is where to add the caption area


# Contains the submit button
submission = wx.Button(left, wx.ID_ANY, label="Submit")
last = wx.BoxSizer(wx.HORIZONTAL)
last.Add(submission, 4, wx.EXPAND)





### TODO: finish reorganising the code from this part down
directory = ""
chosen = False
global amount
amount = 0

# Leaving this image replacement method within the main file due to heavy reliance on UI components
def replaceWithImage(image):
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

# Leaving this directory method in the main file due to heavy reliance on UI components
def dirClicked(event):
	dialogue = wx.Dirdialoguelog(container, "Choose the parent directory", "C:/", 0, (10,10), wx.Size(400,300))
    	complete_request = dialogue.ShowModal()
    	if complete_request == wx.ID_OK:
        	directory = dialogue.GetPath()
        	selection.SetLabel(directory)
        	file_name_pattern.pattern(directory)
        	return directory
    	elif complete_request != wx.ID_OK:
    		directory = ""
    		return directory


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
	saveImage(getName(file_name_holder))
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

dirClicked("Open")

window.MainLoop()
exit()