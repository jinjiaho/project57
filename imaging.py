from PIL import Image
import os, sys

## A library for all your image manipulation needs!
## Requires Pillow for Python 2.7/3.3+

class Imaging(object):

    # set proposed dimension of thumbnail
    # assume max height/width of 255
    def __init__(self, dim=255, path="static/img/items/"):
        self.dim = dim
        self.path = path

    # create thumbnail of size `dim` for file args
    def thumb(self, *args):
        for infile in args:

            infile_abs = self.path + infile
            outfile = os.path.splitext(infile)[0] + ".thumb"
            outfile_abs = self.path + outfile

            if infile != outfile:
                try:
                    im = Image.open(infile_abs)
                    im.thumbnail((self.dim, self.dim), Image.ANTIALIAS)
                    im.save(outfile_abs, "JPEG")
                    return outfile
                except IOError:
                    print("PYTHON: Cannot create thumbnail for '%s'" % infile)

    def __str__(self):
        return "Dimension: %d\nPath: %s" % self.dim, self.path

if __name__ == '__main__':
    print("PYTHON: `Imaging.py` is not meant to be executed directly")