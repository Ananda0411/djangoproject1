from django.contrib import admin
from django.urls import path
from watchapp import views
from django.conf import settings
from django.conf.urls.static import static
from .views import forget_password

urlpatterns = [
    path('stud',views.stud),
    path('dashboard',views.dashboard),
    path('delete/<rid>',views.delete),
    path('edit/<rid>',views.edit),
    path('home',views.home),
    path('pdetails/<pid>',views.product_details),
    path('about',views.about),
    path('contact',views.contact),
    path('cart',views.cart),
    path('placeorder',views.placeorder),
    path('index_online',views.index_online),
    path('register',views.register),
    path('user_login',views.user_login),
    path('user_logout',views.user_logout),
    path('catfilter/<cv>',views.catfilter),
    path('sort/<ap>',views.sort),
    path('range',views.range),
    path('addtocart/<pid>',views.addtocart),
    path('remove/<cid>',views.remove),
    path('viewcart',views.viewcart),
    path('updateqty/<qv>/<cid>',views.updateqty),
    path('makepayment',views.makepayment),
    path('forget/', forget_password, name='forget_password'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
