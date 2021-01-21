import hashlib
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa


def get_filename(filename):
    return filename.upper()


def Attr(cls):
    model = cls.__name__
    return cls.__doc__.replace(model, "").replace("(", "").replace(")", "").replace(" ", "").split(",")

def Hash_parse(text):
    h = hashlib.new("sha256", b"%s"%text)
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


