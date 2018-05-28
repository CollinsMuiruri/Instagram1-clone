from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.latest_images, name='latest'),
    url(r'^search/', views.search_results, name='search_results'),
    url(r'^home/(?P<id>\d+)/$', views.image_detail, name='home'),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^latest/(?P<image_id>\d+)', views.image, name='detail'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^edit/', views.edit, name='edit'),
    url(r'^new/image/$', views.new_image, name='new-image'),
    # url(r'^comment/(?P<pk>\d+)', views.new_comment, name='comment'),
    url(r'^(?P<id>\d+)/$', views.after_detail, name='after'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
