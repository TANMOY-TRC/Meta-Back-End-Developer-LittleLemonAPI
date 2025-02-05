from django.urls import path, include
from . import views


urlpatterns = [
    path('categories/', views.CategoriesView.as_view(), name='categories'),
    path('categories/<int:pk>/', views.CategoriesDetailView.as_view(), name='categories-detail'),

    path('menu-items/', views.MenuItemsView.as_view(), name='menu-items'),
    path('menu-items/<int:pk>/', views.MenuItemDetailView.as_view(), name='menu-item-detail'),

    path('cart/menu-items/', views.CartView.as_view(), name='cart-items'),
    path('cart/menu-items/<int:pk>/', views.CartItemDetailView.as_view(), name='cart-item-detail'),

    path('orders/', views.OrderView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),

    path('groups/manager/users/', views.ManagerGroupListView.as_view(), name='manager-users'),
    path('groups/manager/users/<int:user_id>/', views.ManagerGroupDetailView.as_view(), name='manager-user-detail'),

    path('groups/delivery-crew/users/', views.DeliveryCrewGroupListView.as_view(), name='delivery-crew-users'),
    path('groups/delivery-crew/users/<int:user_id>/', views.DeliveryCrewGroupDetailView.as_view(), name='delivery-crew-user-detail'),
]
