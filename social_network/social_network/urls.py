from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
# This method is used to connect urls-files from different app-packeges:
from django.urls import include, path

# Our main url patterns:
urlpatterns = [
    # For admin panel usage:
    path('admin/', admin.site.urls),
    # Specify that we use for empty url: urls.py file in our main app-packege:
    path('', include('main.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # This statement is for static dir in app useage.

# If we are in DEBUG: 
if settings.DEBUG: 
    # Add one more path for using static graphical filed in media dir: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    