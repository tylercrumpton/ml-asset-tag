import barcode
from barcode.writer import ImageWriter
from PIL import Image

PPI = 300
ROWS = 10
COLS = 5
X_MARGIN = 100
Y_MARGIN = 50
X_SPACING = 20
Y_SPACING = 20

def INCH_TO_PX(inches):
    return int(inches * PPI)

def center(size1, size2):
    return (size1-size2)//2



LABEL_WIDTH = INCH_TO_PX(2.0)
LABEL_HEIGHT = INCH_TO_PX(0.75)

PAGE_WIDTH = INCH_TO_PX(11.0)
PAGE_HEIGHT = INCH_TO_PX(8.5)

test_code = barcode.get("code128", "25600001", writer=ImageWriter())
opts = dict(
    write_text=True,
    module_width=.4,
    module_height=5,
    text_distance=1.5,
    font_size=12,
    quiet_zone=2)
test_image = test_code.render(opts)


single_tag = Image.new('RGB', (LABEL_WIDTH, LABEL_HEIGHT), color="#004ba0")
single_tag.paste(test_image, (center(single_tag.width, test_image.width), 100))


tag_sheet = Image.new('RGB', (PAGE_WIDTH, PAGE_HEIGHT), color="white")
for row in range(ROWS):
    for col in range(COLS):
        x = X_MARGIN + col * (single_tag.width + X_SPACING)
        y = Y_MARGIN + row * (single_tag.height + Y_SPACING)
        tag_sheet.paste(single_tag, (x, y))

tag_sheet.show()



