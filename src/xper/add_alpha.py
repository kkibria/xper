from PIL import Image

def color2RGB(h):
	return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def convertImage(fsrc, xper, fdst):
	img = Image.open(fsrc)
	img = img.convert("RGBA")
	datas = img.getdata()
	newData = []

	modfied = False
	for item in datas:
		if item[0] == xper[0] and item[1] == xper[1] and item[2] == xper[2]:
			newData.append((255, 255, 255, 0))
			modfied = True
		else:
			newData.append(item)
	if modfied:
		img.putdata(newData)
		img.save(fdst, "PNG")
