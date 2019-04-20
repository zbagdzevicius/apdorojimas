from PIL import Image
import math

# path = "image.png"
# path = "noised.png"
path = "image.jpg"
image = Image.open(path)

width = image.width
height = image.height
newimage = Image.new("RGB", (width, height), "white")
for x in range(width):
    for y in range(height):
        pixel_red, pixel_green, pixel_blue = image.getpixel((x,y))
        new_red = 255 - pixel_red
        new_green = 255 - pixel_green
        new_blue = 255 - pixel_blue
        newimage.putpixel((x,y),(new_red,new_green,new_blue))
newimage.show()



def median_filter(image):
    width = image.width
    height = image.height
    members = [(0,0)] * 9
    newimage = Image.new("RGB", (width, height), "white")
    for i in range(1,width-1):
        for j in range(1,height-1):
            members[0] = image.getpixel((i-1,j-1))
            members[1] = image.getpixel((i-1,j))
            members[2] = image.getpixel((i-1,j+1))
            members[3] = image.getpixel((i,j-1))
            members[4] = image.getpixel((i,j))
            members[5] = image.getpixel((i,j+1))
            members[6] = image.getpixel((i+1,j-1))
            members[7] = image.getpixel((i+1,j))
            members[8] = image.getpixel((i+1,j+1))
            members.sort()
            newimage.putpixel((i,j),(members[4]))
    
    newimage.show()

def sobel_filter(image):
    width = image.width
    height = image.height
    newimage = Image.new("RGB", (width, height), "white")
    for x in range(1, width-1):  # ignore the edge pixels for simplicity (1 to width-1)
        for y in range(1, height-1): # ignore edge pixels for simplicity (1 to height-1)

            # initialise Gx to 0 and Gy to 0 for every pixel
            Gx = 0
            Gy = 0

            # top left pixel
            p = image.getpixel((x-1, y-1))
            r = p[0]
            g = p[1]
            b = p[2]

            # intensity ranges from 0 to 765 (255 * 3)
            intensity = r + g + b

            # accumulate the value into Gx, and Gy
            Gx += -intensity
            Gy += -intensity

            # remaining left column
            p = image.getpixel((x-1, y))
            r = p[0]
            g = p[1]
            b = p[2]

            Gx += -2 * (r + g + b)

            p = image.getpixel((x-1, y+1))
            r = p[0]
            g = p[1]
            b = p[2]

            Gx += -(r + g + b)
            Gy += (r + g + b)

            # middle pixels
            p = image.getpixel((x, y-1))
            r = p[0]
            g = p[1]
            b = p[2]

            Gy += -2 * (r + g + b)

            p = image.getpixel((x, y+1))
            r = p[0]
            g = p[1]
            b = p[2]

            Gy += 2 * (r + g + b)

            # right column
            p = image.getpixel((x+1, y-1))
            r = p[0]
            g = p[1]
            b = p[2]

            Gx += (r + g + b)
            Gy += -(r + g + b)

            p = image.getpixel((x+1, y))
            r = p[0]
            g = p[1]
            b = p[2]

            Gx += 2 * (r + g + b)

            p = image.getpixel((x+1, y+1))
            r = p[0]
            g = p[1]
            b = p[2]

            Gx += (r + g + b)
            Gy += (r + g + b)

            # calculate the length of the gradient (Pythagorean theorem)
            length = math.sqrt((Gx * Gx) + (Gy * Gy))

            # normalise the length of gradient to the range 0 to 255
            length = length / 4328 * 255

            length = int(length)

            # draw the length in the edge image
            #newpixel = image.putpixel((length,length,length))
            newimage.putpixel((x,y),(length,length,length))
    newimage.show()

