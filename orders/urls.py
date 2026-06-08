from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),
    path('summary/<int:order_id>/', views.order_summary_view, name='order_summary'),
]
