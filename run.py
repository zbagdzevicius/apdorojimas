from PIL import Image
from threading import Thread
import math
from time import time

class Filter:
    def __init__(self, image_path):
        self.image = Image.open(image_path)
        self.thread_image = None
    
    @staticmethod
    def run(job_fn):
        job_thread = Thread(target=job_fn)
        job_thread.start()

    def effect_negative(self):
        width = self.image.width
        height = self.image.height
        self.thread_image = Image.new("RGB", (width, height), "white")
        for x in range(1, width-1):
            for y in range(1, height-1):
                # get each pixel rgb value
                rgba = self.image.getpixel((x, y))
                # invert rgb values
                pixel_red, pixel_green, pixel_blue = [255 - color_value for color_value in rgba[0:3]]
                # put pixel into empty picture pixel place
                self.thread_image.putpixel((x, y), (pixel_red, pixel_green, pixel_blue))
        self.thread_image.show()
        return self.thread_image

    def filter_median(self):
        width = self.image.width
        height = self.image.height
        members = [(0, 0)] * 9
        newimage = Image.new("RGB", (width, height), "white")
        for i in range(1, width-1):
            for j in range(1, height-1):
                members[0] = self.image.getpixel((i-1, j-1))
                members[1] = self.image.getpixel((i-1, j))
                members[2] = self.image.getpixel((i-1, j+1))
                members[3] = self.image.getpixel((i, j-1))
                members[4] = self.image.getpixel((i, j))
                members[5] = self.image.getpixel((i, j+1))
                members[6] = self.image.getpixel((i+1, j-1))
                members[7] = self.image.getpixel((i+1, j))
                members[8] = self.image.getpixel((i+1, j+1))
                members.sort()
                newimage.putpixel((i, j), (members[4]))
        newimage.show()
        return newimage

    def filter_sobel(self):
        width = self.image.width
        height = self.image.height
        newimage = Image.new("RGB", (width, height), "white")
        for x in range(1, width-1):  # ignore the edge pixels for simplicity (1 to width-1)
            for y in range(1, height-1):  # ignore edge pixels for simplicity (1 to height-1)
                # initialise Gx to 0 and Gy to 0 for every pixel
                Gx = 0
                Gy = 0

                # top left pixel
                p = self.image.getpixel((x-1, y-1))
                r, g, b = p[0:3]

                # intensity ranges from 0 to 765 (255 * 3)
                intensity = r + g + b

                # accumulate the value into Gx, and Gy
                Gx += -intensity
                Gy += -intensity

                # remaining left column
                p = self.image.getpixel((x-1, y))
                r, g, b = p[0:3]

                Gx += -2 * (r + g + b)

                p = self.image.getpixel((x-1, y+1))
                r, g, b = p[0:3]

                Gx += -(r + g + b)
                Gy += (r + g + b)

                # middle pixels
                p = self.image.getpixel((x, y-1))
                r, g, b = p[0:3]

                Gy += -2 * (r + g + b)

                p = self.image.getpixel((x, y+1))
                r, g, b = p[0:3]

                Gy += 2 * (r + g + b)

                # right column
                p = self.image.getpixel((x+1, y-1))
                r, g, b = p[0:3]

                Gx += (r + g + b)
                Gy += -(r + g + b)

                p = self.image.getpixel((x+1, y))
                r, g, b = p[0:3]

                Gx += 2 * (r + g + b)

                p = self.image.getpixel((x+1, y+1))
                r, g, b = p[0:3]

                Gx += (r + g + b)
                Gy += (r + g + b)

                # calculate the length of the gradient (Pythagorean theorem)
                length = math.sqrt((Gx * Gx) + (Gy * Gy))

                # normalise the length of gradient to the range 0 to 255
                length = length / 4328 * 255

                length = int(length)

                # draw the length in the edge image
                newimage.putpixel((x, y), (length, length, length))
        newimage.show()
        return newimage


# path = "img.png"
path = "noised.png"
filter = Filter(image_path=path)
start = time()
filter.filter_median()
end = time()
time_elapsed = end-start
print(time_elapsed)