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
NUM_LABELS_X = 2
NUM_LABELS_Y = 8
BAR_WIDTH = 1.5
BAR_HEIGHT = 41.0
TEXT_Y = 95
BARCODE_Y = 17

LABEL_WIDTH = PAGESIZE[0] / NUM_LABELS_X
LABEL_HEIGHT = PAGESIZE[1] / NUM_LABELS_Y
SHEET_TOP = PAGESIZE[1]

STICKER_ELEMENT_Y_DISTANCE = 15
COLUMN2_X = 180


def label(ean13: str, description: str, sku, color, composition) -> Drawing:
    """
    Generate a drawing with EAN-13 barcode and descriptive text.

    :param composition:
    :param sku:
    :param color:
    :param ean13: The EAN-13 Code.
    :type ean13: str
    :param description: Short product description.
    :type description: str
    :return: Drawing with barcode and description
    :rtype: Drawing
    """

    # First column of sticker
    barcode = Ean13BarcodeWidget(ean13)
    barcode.barWidth = BAR_WIDTH
    barcode.barHeight = BAR_HEIGHT
    x0, y0, bw, bh = barcode.getBounds()
    x_alignment = 10
    barcode.x = x_alignment  # center barcode
    top_element_height = LABEL_HEIGHT / 2
    barcode.y = top_element_height  # spacing from label bottom (pt)

    product_name = String(x_alignment, top_element_height - STICKER_ELEMENT_Y_DISTANCE,
                          description, fontName="Helvetica",
                          fontSize=10)
    color = String(x_alignment, top_element_height - 2 * STICKER_ELEMENT_Y_DISTANCE,
                   "Color: {}".format(color),
                   fontName="Helvetica",
                   fontSize=10)
    composition = String(x_alignment, top_element_height - 3 * STICKER_ELEMENT_Y_DISTANCE, "{}".format(composition),
                         fontName="Helvetica",
                         fontSize=8)

    # Second column of sticker
    column2_y_top = LABEL_HEIGHT / 1.3
    origin_country = String(COLUMN2_X, column2_y_top,
                            "Made in: China", fontName="Helvetica",
                            fontSize=10)
    sku_drawing_element = String(COLUMN2_X, column2_y_top - STICKER_ELEMENT_Y_DISTANCE,
                                 "SKU: {}".format(sku), fontName="Helvetica",
                                 fontSize=10)
    size_text = String(COLUMN2_X, column2_y_top - STICKER_ELEMENT_Y_DISTANCE * 2.8,
                       "Size: ", fontName="Helvetica",
                       fontSize=10)
    size = String(COLUMN2_X + 35, column2_y_top - STICKER_ELEMENT_Y_DISTANCE * 2.8, "{}".format(sku.split("-")[-1]),
                  fontName="Helvetica",
                  fontSize=15, textAnchor="middle")

    label_drawing = Drawing(LABEL_WIDTH, LABEL_HEIGHT)
    label_drawing.add(barcode)
    label_drawing.add(product_name)
    label_drawing.add(color)
    label_drawing.add(composition)
    # Column 2
    label_drawing.add(origin_country)
    label_drawing.add(sku_drawing_element)
    label_drawing.add(size_text)
    label_drawing.add(size)
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
        csv_reader = csv.reader(csv_file, delimiter=';')
        Data = namedtuple("Data", next(csv_reader))  # get names from column headers
        for product_info in map(Data._make, csv_reader):
            canvas = Canvas("label_sheets_with_barcodes-v2/ean-sticker_{}.pdf".format(product_info.EAN13),
                            pagesize=PAGESIZE)

            if len(product_info.EAN13) > 13:
                print("EXITING: EAN code needs to be 13 digits long")
                exit(-1)

            sticker = label(product_info.EAN13, product_info.product_name, product_info.SKU, product_info.color,
                            product_info.composition)
            fill_sheet(canvas, sticker)
            canvas.save()
