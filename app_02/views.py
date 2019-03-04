# from django.core import serializers
from datetime import datetime

from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from rest_framework.response import Response
from rest_framework.views import APIView

# needed modules of step 2
from rest_framework import mixins, generics

from app_02.models import Publisher, Book, Author, User, Token
from app_02.utils.permission import AdministratorPermission
from .serializers import *



from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
# paginator 1: PageNumberPagination
class MyPageNumberPagination(PageNumberPagination):
    # http://127.0.0.1:8000/app02/publisher/?page=1
    page_size = 1   # amount of items per size
    page_query_param = "page"  # parameter within the url to point which page
# paginator 1: LimitOffsetPagination
class MyLimitOffsetPagination(LimitOffsetPagination):
    # http://127.0.0.1:8000/app02/publisher/?limit=1&offset=0
    default_limit = 1

# step 1: use the basic form of APIView of rest_framework
class PublisherView(APIView):

    def get(self, request):
        publishers = Publisher.objects.all()
        # 方式一，使用model_to_dict，然后使用json.dumps()， 略

        # 方式二：使用django自带的序列化器
        # data = serializers.serialize("json", publishers)

        # 方式三:使用restframework的序列化器类 , many 来指明是queryset还是单个model
        # with paginator

        # paginator = MyPageNumberPagination()
        paginator = MyLimitOffsetPagination()
        pubs_with_page = paginator.paginate_queryset(queryset=publishers, request=request, view=self)
        # publishers_serializer = PublisherSerializers(instance=publishers, many=True)
        publishers_serializer = PublisherSerializers(instance=pubs_with_page, many=True)

        # return HttpResponse(publishers_serializer.data)
        return Response(publishers_serializer.data)  # 使用reset_framework 的Response,改Response继承了HttpResponse


class SinglePublisherView(APIView):
    """
    get、put(update)、delete from single book with certain id parameter
    """

    def get(self, request, id):
        # we don't have to figure out 'many' value within the parameters, False is the default value of it
        pub_obj = Publisher.objects.filter(pk=id).first()
        pub_data = PublisherSerializers(instance=pub_obj)
        return Response(pub_data.data)

    def put(self, request, id):
        pub_obj = Publisher.objects.filter(pk=id).first()
        # grasp data from quest and specify parameter 'data' to tell serializer that the object is about to modify
        pub_data = PublisherSerializers(instance=pub_obj, data=request.data)
        if pub_data.is_valid():
            pub_data.save()
            return Response(pub_data.data)
        else:
            return Response(pub_data.errors)

    def delete(self, request, id):
        Publisher.objects.filter(pk=id).delete()
        # return nothing if it's delete function
        return Response()


class BookView(APIView):
    """
    使用rest_framework的APIView， APIView继承了View, 进行了一些简单的封装，request的改变
    """

    # authentication_classes = [TokenAuthentication]          # set the class of authentication
    # permission_classes = [AdministratorPermission]
    # throttle_classes = []

    # parser_classes = []   # set which parser you want to use (more than one is ok)

    def get(self, request):
        books = Book.objects.all()

        # serialize the data of the book , and send it by corresponding serializer that we write above
        # serialized_books = BookSerializers(instance=books, many=True)

        # 1、 another method to get a instance of serializer is using ModelSerializers, that is almost the same
        #  as ModelForm In Form component
        # 2、need to figure out context parameter with request because of our previous setting 'HyperlinkedIdentityField'
        serialized_books = BookModelSerializer(instance=books, many=True, context={"request": request})

        return Response(serialized_books.data)

    def post(self, request):
        # create Book model with the data we give from frontier
        book_obj = BookModelSerializer(data=request.data)
        if book_obj.is_valid():
            # if it's valid, save the object, and return the data
            book_obj.save()
            return Response(book_obj.data)
        else:
            # or return error information
            return Response(book_obj.errors)


class SingleBookView(APIView):
    """
    get、put(update)、delete from single book with certain id parameter
    """

    def get(self, request, id):
        # we don't have to figure out 'many' value within the parameters, False is the default value of it
        book_obj = Book.objects.filter(pk=id).first()
        book_data = BookModelSerializer(instance=book_obj, context={"request": request})
        return Response(book_data.data)

    def put(self, request, id):
        book_obj = Book.objects.filter(pk=id).first()
        # grasp data from quest and specify parameter 'data' to tell serializer that the object is about to modify
        book_data = BookModelSerializer(instance=book_obj, data=request.data)
        if book_data.is_valid():
            book_data.save()
            return Response(book_data.data)
        else:
            return Response(book_data.errors)

    def delete(self, request, id):
        Book.objects.filter(pk=id).delete()
        # return nothing if it's delete function
        return Response()


# step 2: simplify |the process of writing View classes with round-up of mixin and generics


# class AuthorsView(mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView):
#     # set 2 necessary variables to make sure framework work properly
#     queryset = Author.objects.all()
#     serializer_class = AuthorSerializers
#
#     def get(self, request, *args, **kwargs):
#         # run parent's function that has the functionality of get
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
#
# class SingleAuthorView(mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
#                        mixins.UpdateModelMixin, generics.GenericAPIView):
#     # set 2 necessary variables to make sure framework work properly
#     queryset = Author.objects.all()
#     serializer_class = AuthorSerializers
#     lookup_field = "id"
#
#     def get(self, request, *args, **kwargs):
#         # run parent's function that has the functionality of get
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


# step 3: omit functions by follow up a more advanced parent class

class AuthorsView(generics.ListCreateAPIView):
    # set 2 necessary variables to make sure framework work properly
    queryset = Author.objects.all()
    serializer_class = AuthorSerializers


class SingleAuthorView(generics.RetrieveUpdateDestroyAPIView):
    # set 2 necessary variables to make sure framework work properly
    queryset = Author.objects.all()
    serializer_class = AuthorSerializers
    lookup_field = "id"


# step4: final method to write view class, we need to give parameter to as_view() at url like:
# path('authors/', AuthorsModelView.as_view({"get":"list", "post":"create"}), name='authors_view'),
# path('author/<int:id>', AuthorsModelView.as_view({"get":"retrieve", "put":"update", "delete": "destroy"}), ...),


from rest_framework import viewsets
class AuthorsModelView(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializers
    lookup_field = "id"



# ###################################################
# user authorization and limitation of authority
class LoginView(APIView):

    @classmethod
    def get_random_token(cls, user):
        # get md5 value from salt in the md5 generator
        import hashlib
        m = hashlib.md5(user.encode('utf-8'))
        m.update(str(datetime.now()).encode('utf-8'))
        return m.hexdigest()

    def post(self, request):
        """
        check up that if username and password are correct and update or create and then return token
        :return:  token information or error
        """

        result = {"code": "1000", "msg": ""} # 1000：normal , 1001: abnormal
        name = request.data.get("name")
        pwd = request.data.get("pwd")
        user = User.objects.filter(name=name, pwd=pwd).first()
        if user:
            # it's valid
            token = self.get_random_token(user.name)
            Token.objects.update_or_create(user=user, defaults={"token": token})
            result["token"] = token
        else:
            result["code"] = 1001
            result["msg"] = "username or password is invalid!"
        return Response(result)
