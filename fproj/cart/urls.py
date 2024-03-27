from .views import  cart_view
from django.urls import path, include

app_name = 'cart'

urlpatterns = [
    path('', cart_view, name='cart-view'),
    # path('<slug:slug>/', product_detail_view, name='product-detail'),
    # path('search/<slug:slug>/', category_list, name='category-list'),
]