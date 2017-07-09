from PIL import Image

def cropImg(file):
    
    img = Image.open(file)

    # if width > height
    if img.size[0] > img.size[1]:
        b = ((img.size[0] - img.size[1])/2,
             img.size[0] - ((img.size[0] - img.size[1])/2))
        img2 = img.crop((b[0], 0, b[1], img.size[1]))
        img2.save(file)
    
    # if width < height
    elif img.size[0] < img.size[1]:
        b = ((img.size[1] - img.size[0])/2,
             img.size[1] - ((img.size[1] - img.size[0])/2))
        img2 = img.crop((0, b[0], img.size[0], b[1]))
        img2.save(file)

def resizeImg(file, height=200):
    img = Image.open(file)
    if img.size[0] > height:
        hpercent = (height / float(img.size[1]))
        wsize = int((float(img.size[0]) * float(hpercent)))
        img = img.resize((wsize, height), PIL.Image.ANTIALIAS)
        img.save(file)

if __name__ == '__main__':
    print(">>> This is an imaging library and is not meant to be executed directly")