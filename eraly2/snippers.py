import hashlib
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.template.loader import render_to_string
from weasyprint import HTML
from weasyprint.fonts import FontConfiguration

def get_filename(filename):
    return filename.upper()


def Attr(cls):
    model = cls.__name__
    return cls.__doc__.replace(model, "").replace("(", "").replace(")", "").replace(" ", "").split(",")

def Hash_parse(text):
    h = hashlib.new("sha256","%s"%text)
    print(h.digest())
    return h

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

def export_pdf(request, template,contexto={}):
    html = render_to_string(template, contexto)
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline; report.pdf"
    font_config = FontConfiguration()
    HTML(string=html).write_pdf(response, font_config=font_config)
    return response


