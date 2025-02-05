from django.contrib.auth.models import User, Group
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from . import models
from . import filters
from . import serializers
from . import permissions


class CategoriesView(generics.ListCreateAPIView):
    queryset = models.Category.objects.all().order_by('id')
    serializer_class = serializers.CategorySerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            self.throttle_classes = [] # No throttling for GET requests
            return [AllowAny()]
        else:
            return [IsAuthenticated(), permissions.IsManagerOrSuperuser()]


class CategoriesDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Category.objects.all().order_by('id')
    serializer_class = serializers.CategorySerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            self.throttle_classes = [] # No throttling for GET requests
            return [AllowAny()]
        else:
            return [IsAuthenticated(), permissions.IsManagerOrSuperuser()]


class MenuItemsView(generics.ListCreateAPIView):
    queryset = models.MenuItem.objects.all().order_by('id')
    serializer_class = serializers.MenuItemSerializer

    search_fields = ['title']

    def get_permissions(self):
        if self.request.method == 'GET':
            self.throttle_classes = [] # No throttling for GET requests
            return [AllowAny()]
        else:
            return [IsAuthenticated(), permissions.IsManagerOrSuperuser()]


class MenuItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.MenuItem.objects.all().order_by('id')
    serializer_class = serializers.MenuItemSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            self.throttle_classes = [] # No throttling for GET requests
            return [AllowAny()]
        else:
            return [IsAuthenticated(), permissions.IsManagerOrSuperuser()]


class CartView(generics.ListCreateAPIView):
    queryset = models.Cart.objects.all().order_by('id')
    serializer_class = serializers.CartSerializer
    permission_classes = [IsAuthenticated, permissions.IsCustomer]

    def get_queryset(self):
        return models.Cart.objects.filter(user=self.request.user).order_by('id')

    def delete(self, request, *args, **kwargs):
        deleted_count, _ = models.Cart.objects.filter(user=request.user).delete()

        if deleted_count > 0:
            return Response(
                {'detail': f'Successfully cleared {deleted_count} item(s) from the cart.'},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'detail': 'Cart is already empty.'},
                status=status.HTTP_400_BAD_REQUEST
            )


class CartItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Cart.objects.all().order_by('id')
    serializer_class = serializers.CartSerializer
    permission_classes = [IsAuthenticated, permissions.IsCustomer]

    def get_queryset(self):
        return models.Cart.objects.filter(user=self.request.user).order_by('id')


class OrderView(generics.ListCreateAPIView):
    serializer_class = serializers.OrderSerializer
    filterset_class = filters.OrderStatusFilter
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Manager').exists() or user.is_superuser:
            return models.Order.objects.all().order_by('id')
        elif user.groups.filter(name='DeliveryCrew').exists():
            return models.Order.objects.filter(delivery_crew=user).order_by('id')
        return models.Order.objects.filter(user=user).order_by('id')

    def perform_create(self, serializer):
        user = self.request.user
        if not user.groups.exists():
            cart_items = models.Cart.objects.filter(user=self.request.user).order_by('id')
            order = serializer.save(user=self.request.user)
            total_price = 0

            for item in cart_items:
                price = item.menuitem.price * item.quantity
                models.OrderItem.objects.create(
                    order=order,
                    menuitem=item.menuitem,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    price = item.menuitem.price * item.quantity
                )
                total_price += price

            order.total = total_price
            order.save()

            cart_items.delete()

            return order

    def create(self, request, *args, **kwargs):
        cart_items = models.Cart.objects.filter(user=request.user).order_by('id')
        if not cart_items.exists():
            return Response(
                    {'detail': 'Cart is empty.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return super().create(request, *args, **kwargs)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Order.objects.all().order_by('id')
    serializer_class = serializers.OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Manager').exists() or user.is_superuser:
            return models.Order.objects.all().order_by('id')
        elif user.groups.filter(name='DeliveryCrew').exists():
            return models.Order.objects.filter(delivery_crew=user).order_by('id')
        return models.Order.objects.filter(user=user).order_by('id')

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method == 'DELETE' or self.request.method == 'PUT':
            return [IsAuthenticated(), permissions.IsManagerOrSuperuser()]
        else:
            return [IsAuthenticated(), permissions.IsNotCustomer()]


class ManagerGroupListView(generics.ListCreateAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated, permissions.IsManagerOrSuperuser]

    def get_queryset(self):
        return User.objects.filter(groups__name='Manager').order_by('id')

    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        try:
            user = User.objects.get(username=username)
            group, _ = Group.objects.get_or_create(name='Manager')

            if user.groups.filter(name='Manager').exists():
                return Response({'detail': f'User {user.username} is already in Manager group.'},
                                status=status.HTTP_400_BAD_REQUEST)

            user.groups.add(group)
            return Response({'detail': f'User {user.username} added to Manager group.'},
                            status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'},
                            status=status.HTTP_404_NOT_FOUND)

        except Group.DoesNotExist:
            return Response({'detail': 'Manager group not found.'},
                            status=status.HTTP_404_NOT_FOUND)


class ManagerGroupDetailView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, permissions.IsManagerOrSuperuser]

    def destroy(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        try:
            user = User.objects.get(id=user_id)
            group = Group.objects.get(name='Manager')

            if not user.groups.filter(name='Manager').exists():
                return Response({'detail': f'User {user.username} not in Manager group.'},
                                status=status.HTTP_400_BAD_REQUEST)

            user.groups.remove(group)
            return Response({'detail': f'User {user.username} removed from Manager group.'},
                            status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'},
                            status=status.HTTP_404_NOT_FOUND)
        except Group.DoesNotExist:
            return Response({'detail': 'Manager group not found.'},
                            status=status.HTTP_404_NOT_FOUND)


class DeliveryCrewGroupListView(generics.ListCreateAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated, permissions.IsManagerOrSuperuser]

    def get_queryset(self):
        return User.objects.filter(groups__name='DeliveryCrew').order_by('id')

    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        try:
            user = User.objects.get(username=username)
            group, _ = Group.objects.get_or_create(name='DeliveryCrew')

            if user.groups.filter(name='DeliveryCrew').exists():
                return Response({'detail': f'User {user.username} is already in Delivery Crew group.'},
                                status=status.HTTP_400_BAD_REQUEST)

            user.groups.add(group)
            return Response({'detail': f'User {user.username} added to Delivery Crew group.'},
                            status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'},
                            status=status.HTTP_404_NOT_FOUND)

        except Group.DoesNotExist:
            return Response({'detail': 'Delivery Crew group not found.'},
                            status=status.HTTP_404_NOT_FOUND)


class DeliveryCrewGroupDetailView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, permissions.IsManagerOrSuperuser]

    def destroy(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        try:
            user = User.objects.get(id=user_id)
            group = Group.objects.get(name='DeliveryCrew')

            if not user.groups.filter(name='DeliveryCrew').exists():
                return Response({'detail': f'User {user.username} not in Delivery Crew group.'},
                                status=status.HTTP_400_BAD_REQUEST)

            user.groups.remove(group)
            return Response({'detail': f'User {user.username} removed from Delivery Crew group.'},
                            status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'},
                            status=status.HTTP_404_NOT_FOUND)
        except Group.DoesNotExist:
            return Response({'detail': 'Delivery Crew group not found.'},
                            status=status.HTTP_404_NOT_FOUND)
