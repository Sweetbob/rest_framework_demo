from django.db import models

# Create your models here.


class Publisher(models.Model):
    name = models.CharField(max_length=1024)
    email = models.CharField(max_length=1024)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=1024)
    age = models.IntegerField()

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=48)
    price = models.FloatField()
    pub_date = models.DateField()
    publisher = models.ForeignKey("Publisher", on_delete=models.SET_NULL, null=True, blank=True)
    author = models.ManyToManyField("Author")

    def __str__(self):
        return self.title


# ###################################################
# user authorization and limitation of authority


class User(models.Model):
    name = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)

    type_choices = ((1, "ordinary user"), (2, "administrator"),)
    user_type = models.IntegerField(choices=type_choices, default=1)


class Token(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    token = models.CharField(max_length=128)
