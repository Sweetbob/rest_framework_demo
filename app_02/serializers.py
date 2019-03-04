from rest_framework import serializers
from app_02.models import Publisher, Book, Author


class BookSerializers(serializers.Serializer):
    title = serializers.CharField()
    price = serializers.FloatField()
    # pub_date = serializers.DateField()

    # 一对一关联字段，可以用 source 来指定需要显示的数据，不指定将显示对象的__str__值
    publisher = serializers.CharField(source="publisher.name")

    # 一对多或者多对多的字段，可以用source，但是只能显示QuerySet，可以使用SerializerMethodField，然后写一个get__字段的方法，
    # 调用序列化时，会调用这个方法取返回值
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        """
        :param obj: obj is Book's instance here
        :return: what serializers will get when it runs
        """
        author_data = []
        for author_obj in obj.author.all():
            author_data.append(author_obj.name)
        return author_data


class BookModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"

    # replace the value to a url path by using HyperlinkedIdentityField
    # {                                                    {
    #     "id": 1,                                              "id": 1,
    #     "title": "追风筝的人",                                  "title": "追风筝的人",
    #     "price": 23.9,                                        "price": 23.9,
    #     "pub_date": "2015-11-11",        to                   "pub_date": "2015-11-11",
    #     "publisher": 1,                                       "publisher": "http://localhost:8000/app02/publisher/1",
    #     "author": [                                           "author": [
    #         1                                                       1
    #     ]                                                      ]
    # }                                                     }
    Publisher = serializers.HyperlinkedIdentityField(
        # we need to set 'name' for all of the urls, I have no idea why
        view_name="single_publisher_view",
        lookup_field="publisher_id",    # which field you want to converted to
        lookup_url_kwarg="id",          # what you put in on url parameter
    )

    # further more, We can still add custom field display, but we have to overwrite create method to
    # support custom field display
    # publisher = serializers.CharField(source="publisher.pk")

    # def create(self, validated_data):
    #     new_book = Book.objects.create(title=validated_data["title"],
    #                                    price=validated_data["price"],
    #                                    pub_date=validated_data["pub_date"],
    #                                    publisher_id=validated_data["publisher"]["pk"],)
    #     new_book.author.add(*validated_data["author"])
    #     return new_book


class PublisherSerializers(serializers.Serializer):
    """
    使用rest_framwork的方式来创建序列化器，可以序列化 QuerySet 或者 单个model对象
    """
    name = serializers.CharField()
    email = serializers.CharField()


class AuthorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"
