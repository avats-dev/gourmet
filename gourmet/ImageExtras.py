import os, os.path, tempfile, io
from gi.repository import GdkPixbuf, Gtk

try:
    from PIL import Image
except ImportError:
    import Image
from .gdebug import debug

TMPFILE = tempfile.mktemp(prefix='gourmet_tempfile_')

def resize_image (image, width=None, height=None):
    debug("resize_image (self, image, width=None, height=None):",5)
    """Resize an image to have a maximum width=width or height=height.
    We only shrink, we don't grow."""
    iwidth,iheight=image.size
    resized=False
    if width and iwidth > width:
        newheight=int((float(width)/float(iwidth)) * iheight)
        if not height or newheight < height:
            retimage=image.resize((width, newheight))
            resised=True
    if not resized and height and iheight > height:
        newwidth = int((float(height)/float(iheight)) * iwidth)
        retimage = image.resize((newwidth,height))
        resized=True
    if resized:
        return retimage
    else:
        return image

def get_image_from_string(raw: bytes) -> Image.Image:
    """Given raw image data (bytes), return an Image object."""
    if os.name =='posix':
        sfi = io.BytesIO(raw)
        sfi.seek(0)
    else:
        sfi = write_image_tempfile(raw)
    try:
        return Image.open(sfi)
    except:
        print('Trouble in image land.')
        print('We dumped the offending string here:')
        print(sfi)
        print("But we can't seem to load it...")

def get_string_from_image(image: Image.Image) -> bytes:
    """Convert an image into a string representing its JPEG self"""
    ofi = io.BytesIO()
    image = image.convert('RGB')
    image.save(ofi,"JPEG")
    return ofi.getvalue()

def get_pixbuf_from_jpg(raw: bytes) -> GdkPixbuf.Pixbuf:
    """Create a GdkPixbuf.Pixbuf from bytes"""
    glib_bytes = GLib.Bytes.new(raw)
    stream = Gio.MemoryInputStream.new_from_bytes(glib_bytes)
    pixbuf = GdkPixbuf.Pixbuf.new_from_stream(stream)
    return pixbuf
