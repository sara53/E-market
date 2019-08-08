from django.urls import path
from . import views

urlpatterns = [
    path('main', views.mainView),
    path('product', views.productView),
    path('compare', views.compareView),
    path('get_categories', views.getCategories),
    path('get_brands', views.getBrands),
    path('view_all_products', views.viewAllProducts),
    path('view_product', views.view_product),
    path('view_comments', views.view_comments),
    path('add_comment', views.add_comment),
    path('compare_products', views.compare_products),
]
