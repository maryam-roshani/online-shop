from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django_email_verification import urls as mail_urls
from verify_email import urls as verify_email



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
    path('email/', include(mail_urls)),
    path('verification/', include(verify_email)),
]


urlpatterns += staticfiles_urlpatterns()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
