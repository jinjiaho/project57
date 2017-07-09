from PIL import Image
import os, sys

# def thumb(size=255, *args):
#     for infile in args:
#         outfile = os.path.splitext(infile)[0] + ".thumb"
#         if infile != outfile:
#             try:
#                 im = Image.open(infile)
#                 im.thumbnail((size, size), Image.ANTIALIAS)
#                 im.save(outfile, "JPEG")
#             except IOError:
#                 print "PYTHON: Cannot create thumbnail for '%s'" % infile

# if __name__ == '__main__':
#     print("PYTHON: `Imaging.py` is not meant to be executed directly")


print(sys.argv[1:])
size=255
for infile in sys.argv[1:]:
    outfile = os.path.splitext(infile)[0] + ".thumb"
    if infile != outfile:
        try:
            im = Image.open(infile)
            im.thumbnail((size, size), Image.ANTIALIAS)
            im.save(outfile, "JPEG")
        except IOError:
            print "PYTHON: Cannot create thumbnail for '%s'" % infile