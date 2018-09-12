from collections import OrderedDict

from reportlab.graphics import renderPDF
from reportlab.graphics.barcode import eanbc
from reportlab.graphics.shapes import Drawing
from reportlab.pdfgen import canvas


def draw_sticker_items(canvas, start_x=100, start_y=750, step=20):
    new_y = start_y
    sticker_items = OrderedDict({"name": "Elevate Crop Top",
                                 "color": "Color: Black",
                                 "size": "Size: XS",
                                 "sku": "SKU: ECTPU-B-XS"})
    for i, sticker_item in enumerate(sticker_items):
        new_y = start_y - i * step
        canvas.drawString(start_x, new_y, sticker_items[sticker_item])

    return new_y


if __name__ == '__main__':
    c = canvas.Canvas("sticker.pdf")

    startX = 100
    startY = 750
    step = 20
    newY = draw_sticker_items(c, startX, startY, step)

    # draw the eanbc13 code on the Canvas
    barcode_value = "5602897091007"
    barcode_eanbc13 = eanbc.Ean13BarcodeWidget(barcode_value)
    bounds = barcode_eanbc13.getBounds()
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    d = Drawing(50, 10)
    d.add(barcode_eanbc13)
    renderPDF.draw(d, c, startX, newY - 4 * step)

    # Save to file
    c.save()
