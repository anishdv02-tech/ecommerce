from django.urls import path
from store import views


urlpatterns = [
    path('', views.index_view, name='home'),
    path('api/products/', views.get_products, name='api_products'),
    path('api/products/<int:pk>/', views.get_product_detail, name='api_product_detail'),
    path('api/products/create/', views.create_product, name='api_product_create'),
    path('api/products/<int:pk>/update/', views.update_product, name='api_product_update'),
    path('api/products/<int:pk>/delete/', views.delete_product, name='api_product_delete'),
    path('api/categories/', views.get_categories, name='api_categories'),
    path('api/reviews/<int:product_id>/', views.product_reviews, name='api_product_reviews'),
    path('api/coupons/validate/', views.validate_coupon, name='api_validate_coupon'),
    path('api/checkout/', views.checkout, name='api_checkout'),
    path('api/orders/<str:order_number>/', views.get_order_tracking, name='api_order_tracking'),
]


