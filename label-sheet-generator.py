#!/usr/bin/env python3
import csv
from collections import namedtuple

from reportlab.graphics import renderPDF
from reportlab.graphics.barcode.eanbc import Ean13BarcodeWidget
from reportlab.graphics.shapes import Drawing, String
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas

"""
Adjust pagesize, number of labels, barcode size and
positions of barcode and description to your needs.
"""
PAGESIZE = A4
NUM_LABELS_X = 3
NUM_LABELS_Y = 8
BAR_WIDTH = 1.5
BAR_HEIGHT = 51.0
TEXT_Y = 95
BARCODE_Y = 17

LABEL_WIDTH = PAGESIZE[0] / NUM_LABELS_X
LABEL_HEIGHT = PAGESIZE[1] / NUM_LABELS_Y
SHEET_TOP = PAGESIZE[1]


def label(ean13: str, description: str, sku, color) -> Drawing:
    """
    Generate a drawing with EAN-13 barcode and descriptive text.

    :param sku:
    :param color:
    :param ean13: The EAN-13 Code.
    :type ean13: str
    :param description: Short product description.
    :type description: str
    :return: Drawing with barcode and description
    :rtype: Drawing
    """

    stepY = 10
    product_name = String(0, TEXT_Y, description, fontName="Helvetica",
                          fontSize=10, textAnchor="middle")
    product_name.x = LABEL_WIDTH / 2  # center text (anchor is in the middle)

    color_size = String(0, TEXT_Y - stepY, "Color: {}   size: {}".format(color, sku.split("-")[-1]),
                        fontName="Helvetica",
                        fontSize=10, textAnchor="middle")
    color_size.x = LABEL_WIDTH / 2

    sku = String(0, TEXT_Y - stepY * 2, "SKU: {}".format(sku), fontName="Helvetica",
                 fontSize=10, textAnchor="middle")

    sku.x = LABEL_WIDTH / 2

    barcode = Ean13BarcodeWidget(ean13)
    barcode.barWidth = BAR_WIDTH
    barcode.barHeight = BAR_HEIGHT
    x0, y0, bw, bh = barcode.getBounds()
    barcode.x = (LABEL_WIDTH - bw) / 2  # center barcode
    barcode.y = BARCODE_Y  # spacing from label bottom (pt)

    label_drawing = Drawing(LABEL_WIDTH, LABEL_HEIGHT)
    label_drawing.add(product_name)
    label_drawing.add(color_size)
    label_drawing.add(sku)
    label_drawing.add(barcode)
    return label_drawing


def fill_sheet(canvas: Canvas, label_drawing: Drawing):
    """
    Simply fill the given ReportLab canvas with label drawings.

    :param canvas: The ReportLab canvas
    :type canvas: Canvas
    :param label_drawing: Contains Drawing of configured size
    :type label_drawing: Drawing
    """
    for u in range(0, NUM_LABELS_Y):
        for i in range(0, NUM_LABELS_X):
            x = i * LABEL_WIDTH
            y = SHEET_TOP - LABEL_HEIGHT - u * LABEL_HEIGHT
            renderPDF.draw(label_drawing, canvas, x, y)


if __name__ == '__main__':

    with open('product_info.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        Data = namedtuple("Data", next(csv_reader))  # get names from column headers
        for product_info in map(Data._make, csv_reader):
            canvas = Canvas("label_sheets_with_barcodes/ean-sticker_{}.pdf".format(product_info.EAN13),
                            pagesize=PAGESIZE)
            sticker = label('5432072586067', product_info.product_name, product_info.SKU, product_info.color)
            fill_sheet(canvas, sticker)
            canvas.save()
