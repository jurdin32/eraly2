import datetime
import hashlib
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.template.loader import render_to_string
from weasyprint import HTML
from weasyprint.fonts import FontConfiguration

import uuid
from PIL import Image
from io import BytesIO
from django.core.files import File
from django.core.files.base import ContentFile
from django.db import models

from Producto import models


def get_filename(filename):
    return filename.upper()


def Attr(cls):
    model = cls.__name__
    return cls.__doc__.replace(model, "").replace("(", "").replace(")", "").replace(" ", "").split(",")

def Hash_parse(text):
    fecha=str(datetime.datetime.now()).replace(' ','').replace(",","").replace(".","").replace(':','').replace('-','')
    text =fecha+text
    print(text)
    h = hashlib.sha256(str(text).encode('utf-8')).hexdigest()
    return h


#no sirve
def render_pdf_view(request,page,contexto={}):
    template_path = page
    context = contexto
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response,link_callback="/document/")
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

#pdf
def export_pdf(request, template,contexto={}):
    html_string = render_to_string(template, contexto)
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline; documento.pdf"
    font_config = FontConfiguration()
    html.write_pdf(response, font_config=font_config)
    return response

#redimensionar imagen:
class ResizeImageMixin:
    def resize(self, imageField, size:tuple):
        im = Image.open(imageField)  # Catch original
        source_image = im.convert('RGB')
        source_image=source_image.resize(size)  # Resize to size
        output = BytesIO()
        source_image.save(output, format='JPEG',optimize=True, quality=55) # Save resize image to bytes
        output.seek(0)
        content_file = ContentFile(output.read())  # Read output and create ContentFile in memory
        file = File(content_file)
        random_name = f'{uuid.uuid4()}.jpeg'
        imageField.save(random_name, file, save=False)

