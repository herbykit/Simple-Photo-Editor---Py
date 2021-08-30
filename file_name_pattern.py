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
