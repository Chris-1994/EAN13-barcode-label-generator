from flask import Flask, render_template, request, make_response
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas

app = Flask(__name__)
from LabelSheetGenerator import LabelSheetGenerator

app.labelGenerator = LabelSheetGenerator()


@app.route('/')
def index():
    return render_template('index.html', page_title='Famme dev')


@app.route('/generate_barcodes')
def generate_barcodes():
    product = request.args.get("product")
    sku = request.args.get("SKU")
    ean13 = request.args.get("EAN13")
    color = request.args.get("color")
    composition = request.args.get("composition")
    origin = request.args.get("origin")
    filename = "{}_{}_ean-sticker.pdf".format(sku, ean13)
    canvas = Canvas(filename,
                    pagesize=A4)

    sticker = app.labelGenerator.label(ean13,
                                       product,
                                       sku,
                                       color,
                                       composition,
                                       origin)
    app.labelGenerator.fill_sheet(canvas, sticker)

    canvas.save()
    pdf_out = canvas.getpdfdata()
    response = make_response(pdf_out)
    response.headers['Content-Disposition'] = "attachment; filename={}".format(filename)
    response.mimetype = 'application/pdf'
    return response


if __name__ == '__main__':
    app.run()
