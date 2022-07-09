from django.urls import path
from .views import login_view,log_out,register,update_view,delete_view,contact

urlpatterns = [
    path('login/',login_view,name='login'),
    path('logout/',log_out,name='logout'),
    path('register/',register,name='register'),
    path('update/',update_view,name='update'),
    path('delete/',delete_view,name='delete'),
    path('contact/',contact,name='contact')
    ]
