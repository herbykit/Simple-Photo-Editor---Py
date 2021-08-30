def saveImage(asname):
	global editer, currentImage
	editer.save(os.path.dirname(currentImage)+"//Edited Photos//"+asname+"TV.JPG")
	shutil.move(currentImage, os.path.dirname(currentImage)+"//Original Photos//"+asname+".JPG")
	if os.path.exists(currentImage):
		print("No more picture files in directory")
		exit()

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

def getName():
	global fileNameHolder
	TOOMUCH = fileNameHolder.GetValue()
	return TOOMUCH

