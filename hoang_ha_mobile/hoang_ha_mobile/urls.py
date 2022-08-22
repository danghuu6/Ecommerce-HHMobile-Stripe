"""hoang_ha_mobile URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin-site/', admin.site.urls),

    path('admin/accounts/', include('accounts.administrator.urls')),
    path('customer/accounts/', include('accounts.customer.urls')),
    path('accounts/', include('accounts.guest.urls')),

    path('admin/articles/', include('articles.administrator.urls')),
    path('customer/articles/', include('articles.customer.urls')),
    path('articles/', include('articles.guest.urls')),

    path('admin/carts/', include('carts.administrator.urls')),
    path('customer/carts/', include('carts.customer.urls')),
    path('carts/', include('carts.guest.urls')),

    path('admin/categories/', include('categories.administrator.urls')),
    path('customer/categories/', include('categories.customer.urls')),
    path('categories/', include('categories.guest.urls')),

    path('admin/orders/', include('orders.administrator.urls')),
    path('customer/orders/', include('orders.customer.urls')),
    path('orders/', include('orders.guest.urls')),

    path('admin/products/', include('products.administrator.urls')),
    path('customer/products/', include('products.customer.urls')),
    path('products/', include('products.guest.urls')),

    path('admin/tags/', include('tags.administrator.urls')),
    # path('customer/tags/', include('tags.customer.urls')),
    path('tags/', include('tags.guest.urls')),

    path('admin/variants/', include('variants.administrator.urls')),
    path('customer/variants/', include('variants.customer.urls')),
    path('variants/', include('variants.guest.urls')),

    path('admin/comments/', include('comments.administrator.urls')),
    path('customer/comments/', include('comments.customer.urls')),
    path('comments/', include('comments.guest.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
