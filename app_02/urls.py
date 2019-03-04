"""CBV URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include
from app_02.views import *
from rest_framework import routers

# otherwise, we can include urls by registering with router provided by rest_framework
router = routers.DefaultRouter()
router.register("authors", AuthorsModelView)


urlpatterns = [
    path('publisher/', PublisherView.as_view(), name='publishers_view'),
    path('publisher/<int:id>', SinglePublisherView.as_view(), name="single_publisher_view"),

    path('books/', BookView.as_view(), name='books_view'),
    path('book/<int:id>', SingleBookView.as_view(), name='single_book_view'),

    # path('authors/', AuthorsView.as_view(), name='authors_view'),
    # path('author/<int:id>', SingleAuthorView.as_view(), name='single_author_view'),

    # path('authors/', AuthorsModelView.as_view({"get": "list", "post": "create"}), name='authors_view'),
    # path('author/<int:id>', AuthorsModelView.as_view({"get":"retrieve", "put":"update", "delete": "destroy"}), name='single_author_view'),

    # format with router
    path("", include(router.urls)),

    path('login/', LoginView.as_view(), name='login_view'),
]
