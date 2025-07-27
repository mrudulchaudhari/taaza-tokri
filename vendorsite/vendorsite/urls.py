from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import landing_page_view

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Include all apps from both branches
    path('accounts/', include('accounts.urls')),
    path('supplier/', include('supplier.urls')),
    path('vendor/', include('vendor.urls')),
    path('listings/', include('listings.urls')), # From your friend's branch
    path('reviews/', include('reviews.urls')),   # From your friend's branch

    # Use your landing page as the homepage
    path('', landing_page_view, name='landing'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
