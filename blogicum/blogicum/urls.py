from django.conf.urls import handler403, handler404, handler500
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from blog import views


handler403 = 'pages.views.custom_403'
handler404 = 'pages.views.custom_404'
handler500 = 'pages.views.custom_500'


urlpatterns = [
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/registration/', views.register, name='registration'),
    path('admin/', admin.site.urls),
    path('', include('blog.urls', namespace='blog')),
    path('pages/', include('pages.urls', namespace='pages')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )