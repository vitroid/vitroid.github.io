# https://stackoverflow.com/questions/7460218/get-image-size-without-downloading-it-in-python

import urllib.request
from PIL import ImageFile
from logging import getLogger, basicConfig, INFO, DEBUG

def getsizes(uri):
    # get file size *and* image size (None if not known)
    logger = getLogger()
    logger.info(uri)
    try:
        file = urllib.request.urlopen(uri)
        size = file.headers.get("content-length")
        if size: 
            size = int(size)
        p = ImageFile.Parser()
        while True:
            data = file.read(1024)
            if not data:
                break
            p.feed(data)
            if p.image:
                return size, p.image.size
        file.close()
    except:
        return None
    return(size, None)

if __name__ == "__main__":
    print(getsizes("https://live.staticflickr.com/7917/46611114124_54653d669c_k_d.jpg"))
