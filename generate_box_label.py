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


def draw_box_number(canvas, x, y, box_number):
    sticker_items = OrderedDict({
        "box": f"BOX {box_number}",
    },
    )
    for i, sticker_item in enumerate(sticker_items):
        canvas.drawString(x, y, sticker_items[sticker_item], )


def draw_line(canvas, x, y):
    sticker_items = OrderedDict({
        "line": "---------------------------------------------------------------------------",
    },
    )
    for i, sticker_item in enumerate(sticker_items):
        canvas.drawString(x, y, sticker_items[sticker_item], )


def create_sticker_for_box(sticker_name="sticker.pdf", box_number=1):
    c = canvas.Canvas(sticker_name)
    c.setFont("Helvetica", 9)
    startX = 100
    startY = 780
    draw_box_number(c, startX, startY + 30, box_number)
    step = 12
    draw_line(c, startX, startY + step)

    with open('store_order.csv') as packing_information_csv:
        packing_information = csv.reader(packing_information_csv, delimiter=',')
        next(packing_information)  # skip header row
        for line in packing_information:
            if len(line) == 0:
                continue  # probably just an empty line
            box_number_from_csv = line[4]
            if box_number != int(box_number_from_csv):
                continue

            if line[3] == '0':
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


num_boxes = 2
for i in range(1, num_boxes + 1):
    create_sticker_for_box(f"box_{i}.pdf", box_number=i)
