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
# Defining the base directory as an empty string to avoid issues with null values
directory = ""
# Defines an image variable for use across functions different from currentImage
global edited_image


##### Building the GUI #####
window = wx.App(False);
currentImage = wx.Image(1,1)
container = wx.Frame(None, wx.ID_ANY, "Picture Editing")
container.Maximize()
left = wx.Panel(container, wx.ID_ANY)
right = wx.Panel(container, wx.ID_ANY)
bothSidesContainer = wx.BoxSizer(wx.HORIZONTAL)
bothSidesContainer.Add(left, 1, wx.ALIGN_LEFT | wx.EXPAND)
bothSidesContainer.Add(right, 3, wx.EXPAND)
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

## Captions section
caption_text_holder = wx.StaticText(left, wx.ID_ANY, "Input caption here:")
caption_textbox = wx.TextCtrl(left, wx.ID_ANY, "")
caption1 = wx.BoxSizer(wx.HORIZONTAL)
caption2 = wx.BoxSizer(wx.HORIZONTAL)
caption1.Add(caption_text_holder)
caption1.Add(caption_textbox)

# Applies text to the image when clicked; possibly TODO to move into function
for iteration_for_name in ["Black","White"]:
	selected_color = wx.Button(left,wx.ID_ANY,label=iteration_for_name)
	caption2.Add(selected_color)
	def addText(name=selected_color):
		global editer
		global showImage
		if name == "White":
			color=(255,255,255)
		elif name == "Black":
			color=(0,0,0)
		edited_image = ImageDraw.Draw(editer)
		edited_image.text((0,editer.size[1]),text=caption_textbox.GetValue(),font=ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf',18),fill=color)
		new_image_value = wx.Image(editor.size[0],editer.size[1])
		new_image_value.SetData(edited_image.convert('RGB').tostring())
		for old_image_values in right.GetChildren():
			old_image_values.Destroy()
		rightOrganiser.Add(new_image_value, 1, wx.ALIGN_CENTER | wx.EXPAND)
	selected_color.Bind(wx.EVT_BUTTON, addText)


# Contains the submit button
submission = wx.Button(left, wx.ID_ANY, label="Submit")
last = wx.BoxSizer(wx.HORIZONTAL)
last.Add(submission, 4, wx.EXPAND)


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
	dialogue = wx.DirDialog(container, "Choose the parent directory", "C:/", 0, (10,10), wx.Size(400,300))
	complete_request = dialogue.ShowModal()
	if complete_request == wx.ID_OK:
		directory = dialogue.GetPath()
		selection.SetLabel(directory)
		file_name_pattern.pattern(directory)
		return directory
	elif complete_request != wx.ID_OK:
		directory = ""
		return directory

# Finish working with the image and save it to a file
def submitting(takeit):
	global currentImage
	saveImage(getName(file_name_holder))
	pattern(os.path.dirname(currentImage))


### The closing code for finishing with creating the UI ###
left.Bind(wx.EVT_BUTTON, submitting, submission)
resizing.Bind(wx.EVT_BUTTON, functions.resizeIt)
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