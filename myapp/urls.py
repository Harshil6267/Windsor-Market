from django.urls import path
from myapp import views

app_name = 'myapp'
urlpatterns = [ path(r'index/', views.index, name='index'),
                path(r'about/', views.about, name='about'),
                path(r'<cat_no>',views.detail,name='detail'),
                path(r'products/', views.products, name='products'),
                path(r'place_order/', views.place_order, name='place_order'),
                path(r'products/<prod_id>', views.productdetail, name='productdetail'),
                path(r'login/', views.user_login, name='user_login'),
                path(r'logout/', views.user_logout, name='user_logout'),
                path(r'myorders/', views.myorders, name='my_order'),
                path(r'register/', views.register, name='register'),
                path(r'profile/', views.profile, name='profile')
             ]
