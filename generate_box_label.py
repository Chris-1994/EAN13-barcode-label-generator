import csv
from collections import OrderedDict

from reportlab.graphics import renderPDF
from reportlab.graphics.barcode import eanbc
from reportlab.graphics.shapes import Drawing
from reportlab.pdfgen import canvas


def draw_sticker_items(canvas, sticker_items, start_x=100, start_y=0, step=30):
    new_y = start_y
    for i, sticker_item in enumerate(sticker_items):
        new_y = start_y - i * step
        canvas.drawString(start_x, new_y, sticker_items[sticker_item])

    return new_y - 15


def draw_box_number(canvas, x, y):
    sticker_items = OrderedDict({
        "box": "BOX 1",
    },
    )
    for i, sticker_item in enumerate(sticker_items):
        canvas.drawString(x, y, sticker_items[sticker_item], )


def draw_line(canvas, x, y):
    sticker_items = OrderedDict({
        "box": "---------------------------------------------------------------------------",
    },
    )
    for i, sticker_item in enumerate(sticker_items):
        canvas.drawString(x, y, sticker_items[sticker_item], )


c = canvas.Canvas("sticker.pdf")
c.setFont("Helvetica", 9)
startX = 100
startY = 780
draw_box_number(c, startX, startY + 30)
step = 12
draw_line(c, startX, startY + step)

with open('store_order.csv') as packing_information_csv:
    packing_information = csv.reader(packing_information_csv, delimiter=',')
    next(packing_information)  # skip header row
    for line in packing_information:
        if line[3] == 0:
            continue  # probably did not have the item
        sticker_items = OrderedDict({"sku": f'SKU: {line[0]} –– Title: {line[1]} –– quantity: {line[3]}',
                                     "fill": "---------------------------------------------------------------------------",
                                     },
                                    )
        newY = draw_sticker_items(c, sticker_items, startX, startY, step)
        startY = newY

d = Drawing(50, 10)
renderPDF.draw(d, c, startX, newY - 4 * step)

# Save to file
c.save()
