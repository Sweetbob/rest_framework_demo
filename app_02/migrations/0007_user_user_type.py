# Generated by Django 2.1.7 on 2019-02-26 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_02', '0006_auto_20190224_2322'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_type',
            field=models.IntegerField(choices=[(1, 'ordinary user'), (2, 'administrator')], default=1),
        ),
    ]
