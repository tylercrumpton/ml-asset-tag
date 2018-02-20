import barcode
from barcode.writer import ImageWriter
from PIL import Image, ImageDraw

def INCH_TO_PX(inches):
    return int(inches * PPI)

PPI = 300
ROWS = 10
COLS = 5
X_MARGIN = INCH_TO_PX(0.0625)
Y_MARGIN = INCH_TO_PX(0.0625)
X_SPACING = INCH_TO_PX(0.05)
Y_SPACING = INCH_TO_PX(-0.05)

TAG_WIDTH = INCH_TO_PX(2.0)
TAG_HEIGHT = INCH_TO_PX(0.75)

PAGE_WIDTH = INCH_TO_PX(11.0)
PAGE_HEIGHT = INCH_TO_PX(8.5)

def center(size1, size2):
    return (size1-size2)//2

def generate_barcode(number):
    barcode_image = barcode.get("code128", str(number), writer=ImageWriter())
    opts = dict(
        write_text=True,
        module_width=.4,
        module_height=5,
        text_distance=1.5,
        font_size=12,
        quiet_zone=2)
    return barcode_image.render(opts)

def generate_single_tag(number, template):
    barcode_image = generate_barcode(number)
    template.paste(barcode_image, (center(template.width, barcode_image.width), 120))
    return template

def generate_tag_outline(image):
    draw = ImageDraw.Draw(image)
    start = (center(image.width, TAG_WIDTH), center(image.height, TAG_HEIGHT))
    draw.rectangle([start, (start[0] + TAG_WIDTH, start[1] + TAG_HEIGHT)], outline="grey")
    del draw
    return image

numbers = range(25600001, 25600001+ROWS*COLS)

template = Image.open("template.png")

tag_sheet = Image.new('RGB', (PAGE_WIDTH, PAGE_HEIGHT), color="white")
for row in range(ROWS):
    for col in range(COLS):
        tag = generate_single_tag(numbers[row*COLS+col], template)
        tag = generate_tag_outline(tag)
        x = X_MARGIN + col * (tag.width + X_SPACING)
        y = Y_MARGIN + row * (tag.height + Y_SPACING)
        tag_sheet.paste(tag, (x, y))

tag_sheet.show()
tag_sheet.save("sheet.png")



