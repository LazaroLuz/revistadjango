from django.db import models
from stdimage.models import StdImageField

from django.db.models import signals
from django.template.defaultfilters import slugify


class Base(models.Model):
    criado = models.DateTimeField('Data de criação', auto_now_add=True)
    modificado = models.DateTimeField('Data de Atualização', auto_now=True)

    class Meta:
        abstract = True


class Comic(Base):
    name = models.CharField('Nome', max_length=100, unique=True)
    description = models.TextField('Description')
    # picture = StdImageField('imagem', upload_to="rvt/%d/%m/%Y", variations={'thumb': (280, 380)})  #  variations={'thumb': (x,y)}
    picture = models.CharField('Picture', max_length=255)
    slug = models.SlugField('Slug', max_length=100, editable=False)

    def __str__(self):
        return self.name


class Revista(Base):
    base = models.ForeignKey(Comic, on_delete=models.CASCADE)
    # imagem = models.ImageField('revista', upload_to="revista")
    # file = models.FileField(upload_to=f"revista/%d/%m/%Y",)
    file = models.CharField('File', max_length=255)

    def __str__(self):
        return self.file


def comic_pre_save(signal, instance, sender, **kwargs):
    instance.slug = slugify(instance.name)


signals.pre_save.connect(comic_pre_save, sender=Comic)
