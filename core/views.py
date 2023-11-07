from django.views.generic import TemplateView, ListView
from django.views.generic.edit import FormView
from .models import Comic, Revista
from .forms import ComicForm, RevistaForm, FileFieldForm
from webscrapy.main import link_to_image, web_link

# Create your views here.


class IndexViews(ListView):
    template_name = 'index.html'
    model = Comic
    paginate_by = 23
    ordering = 'name'


class HqViews(TemplateView):
    template_name = 'hq.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comics'] = Comic.objects.get(slug=context['slug'])
        context['galeria'] = Revista.objects.filter(base_id=context['comics'].id)

        return context


class FlipViews(TemplateView):
    template_name = 'flip.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['comics'] = Comic.objects.get(slug=context['slug'])
        context['galeria'] = Revista.objects.filter(base_id=context['comics'].id)

        return context


class ComicViews(FormView):
    form_class = ComicForm
    template_name = 'comic.html'
    success_url = "revista"

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        # files = request.FILES.getlist("file_field")
        if form.is_valid():
            form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class FileFieldFormView(FormView):
    form_class = FileFieldForm
    template_name = 'upload.html'
    success_url = "upload"  # Replace with your URL or reverse().

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            link = form.cleaned_data["url"]
            web_link(link=link)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class RevistaViews(FormView):
    form_class = RevistaForm
    template_name = "revista.html"  # Replace with your template.
    success_url = "comic"  # Replace with your URL or reverse().

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist("file")

        if form.is_valid():
            base = form.cleaned_data["base"]
            for f in files:
                revista = Revista(base=base, file=f)  # Do something with each file.
                revista.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

