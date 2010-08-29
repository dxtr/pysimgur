#!/usr/bin/python

import sys
import urllib
import base64
try:
    import simplejson as json
except ImportError:
    import json
from urlparse import urlparse

try:
    import gtk.gdk
    GTK_GDK = True
except ImportError:
    GTK_GDK = False

apikey="4fce3ffabb20d0faad995feee3e909ba"

class simgur: # s for simple :)
    def __init__(self,apikey=None):
        self.apikey = apikey

    def upload(self,image):
        if self.apikey is None:
            raise Exception, "No API key is specified"
            return None
        else:
            pdata = {'key': self.apikey,
                     'image': base64.b64encode(image)}
            response = urllib.urlopen('http://imgur.com/api/upload.json',
                                      urllib.urlencode(pdata))
            return json.loads(response.read())
            
    def upload_from_url(self,url):
        if self.apikey is None:
            raise Exception, "No API Key is specified"
            return None
        else:
            pdata = {'key': self.apikey,
                     'image': url}
            response = urllib.urlopen('http://imgur.com/api/upload.json',
                                      urllib.urlencode(pdata))
            return json.loads(response.read())

def GtkGrabScreen():
    filename = "screenshot.png"
    w = gtk.gdk.get_default_root_window()
    sz = w.get_size()
    pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8,sz[0],sz[1])
    pb = pb.get_from_drawable(w,w.get_colormap(),0,0,0,0,sz[0],sz[1])
    if (pb != None):
        pb.save("screenshot.png","png")
        return filename
    else:
        return None

def main(argv):
    imgapi = simgur(apikey)
    if len(argv) >= 1:
        for x in argv:
            o = urlparse(x)
            upload = None
            print "Uploading %s..." % o.geturl()
            if o.scheme == 'http': # Upload from url
                upload = imgapi.upload_from_url(o.geturl())['rsp']
            elif o.scheme == '': # Probably a local file
                with open(o.geturl(),'r') as f:
                    data = f.read()
                    upload = imgapi.upload(data)['rsp']
            else:
                "[ERROR] Unsupported scheme: %s" % o.scheme
                continue

            if upload['stat'] == 'fail':
                print "Failed to upload image (%s): %s" % (upload['image']['error_code'],upload['image']['error_msg'])
                continue
            elif upload['stat'] == 'ok':
                print 'Uploaded the image!'
                print "Image: %s" % upload['image']['original_image']
                print "Large thumbnail: %s" % upload['image']['large_thumbnail']
                print "Small thumbnail: %s" % upload['image']['small_thumbnail']
                print "Imgur page: %s" % upload['image']['imgur_page']
                print "Delete page: %s" % upload['image']['delete_page']
        return 1
    else: # What should we do here? Take a screenshot and upload?
        if GTK_GDK == True:
            print "Taking screenshot with PyGtk..."
            ss = GtkGrabScreen()
            if ss == None:
                print "Failed!"
                return 0
            else:
                print "Success!"
                return main([ss])
        else:
            print "I... I.. I don't really know what to do."
            print "I got no arguments but I can't take any screenshots because we don't seem to have pygtk installed"
            return 0

if __name__ == "__main__":
    main(sys.argv[1:])
