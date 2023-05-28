from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('',views.home),
    path('login',views.login_page,name='login-page'),
    path('register',views.userregister,name='register-page'),
    path('save_register',views.save_register,name='register-user'),
    path('user_login',views.login_user,name='login-user'),
    path('home',views.home,name='home-page'),
    path('logout',views.logout_user,name='logout'),
    path('profile',views.profile,name='profile-page'),
    path('update_password',views.update_password,name='update-password'),
    path('update_profile',views.update_profile,name='update-profile'),
    path('petrol_list',views.petrol_list,name='petrol-page'),
    path('manage_petrol',views.manage_petrol,name='manage-petrol'),
    path('manage_petrol/<int:pk>',views.manage_petrol,name='manage-petrol-pk'),
    path('view_petrol/<int:pk>',views.view_petrol,name='view-petrol-pk'),
    path('delete_petrol/<int:pk>',views.delete_petrol,name='delete-petrol-pk'),
    path('save_petrol',views.save_petrol,name='save-petrol'),
    path('stock_list',views.stock_list,name='stock-page'),
    path('manage_stock',views.manage_stock,name='manage-stock'),
    path('manage_stock/<int:pk>',views.manage_stock,name='manage-stock-pk'),
    path('view_stock/<int:pk>',views.view_stock,name='view-stock-pk'),
    path('delete_stock/<int:pk>',views.delete_stock,name='delete-stock-pk'),
    path('save_stock',views.save_stock,name='save-stock'),
    path('inventory',views.inventory,name='inventory-page'),
    path('sale_list',views.sale_list,name='sale-page'),
    path('manage_sale',views.manage_sale,name='manage-sale'),
    path('manage_sale/<int:pk>',views.manage_sale,name='manage-sale-pk'),
    path('view_sale/<int:pk>',views.view_sale,name='view-sale-pk'),
    path('delete_sale/<int:pk>',views.delete_sale,name='delete-sale-pk'),
    path('save_sale',views.save_sale,name='save-sale'),
    path('sales_report',views.sales_report,name='sales-report-page'),
    path('sales_report/<str:rep_date>',views.sales_report),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
