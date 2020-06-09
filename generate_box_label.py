import csv
from collections import OrderedDict

from reportlab.graphics import renderPDF
from reportlab.graphics.barcode import eanbc
from reportlab.graphics.shapes import Drawing
from reportlab.pdfgen import canvas


def draw_sticker_items(canvas, start_x=100, start_y=0, step=30):
    new_y = start_y
    sticker_items = OrderedDict({"sku": "SKU: SVHWL-BK-XS",
                                 "title": "Title: 7/8 Black Vortex Leggings",
                                 "quantity": "Quantity: 1",
                                 "fill": "---------------------------------------------------------------------------",
                                 },
                                )
    for i, sticker_item in enumerate(sticker_items):
        new_y = start_y - i * step
        canvas.drawString(start_x, new_y, sticker_items[sticker_item])

    return new_y - 30


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


if __name__ == '__main__':
    c = canvas.Canvas("sticker.pdf")

    startX = 100
    startY = 750
    draw_box_number(c, startX, startY + 40)
    step = 15
    draw_line(c, startX, startY + step)

    with open('store_order.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')

    for i in range(5):
        newY = draw_sticker_items(c, startX, startY, step)
        startY = newY

    d = Drawing(50, 10)
    renderPDF.draw(d, c, startX, newY - 4 * step)

    # Save to file
    c.save()
