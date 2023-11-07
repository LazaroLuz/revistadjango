from django.urls import path
from .views import IndexViews, HqViews, ComicViews, FileFieldFormView, RevistaViews, FlipViews


urlpatterns = [
    path('', IndexViews.as_view(), name='index'),
    path('hq/<slug>/', HqViews.as_view(), name='hq'),
    path('flip/<slug>/', FlipViews.as_view(), name='flip'),
    path('comic', ComicViews.as_view(), name='comic'),
    path('revista', RevistaViews.as_view(), name='revista'),
    path('upload', FileFieldFormView.as_view(), name='upload'),
]
