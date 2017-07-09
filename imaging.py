from PIL import Image
import os, sys

def thumb(size=285, *args):
    for infile in args:
        outfile = os.path.splitext(infile)[0] + ".thumbnail"
        if infile != outfile:
            try:
                im = Image.open(infile)
                im.thumbnail((size, size), Image.ANTIALIAS)
                im.save(outfile, "JPEG")
            except IOError:
                print "PYTHON: Cannot create thumbnail for '%s'" % infile

if __name__ == '__main__':
    print("PYTHON: `Imaging.py` is not meant to be executed directly")