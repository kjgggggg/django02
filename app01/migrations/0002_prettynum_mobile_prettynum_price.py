# Generated by Django 4.1 on 2022-08-22 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='prettynum',
            name='mobile',
            field=models.CharField(max_length=11, null=True, verbose_name='手机号'),
        ),
        migrations.AddField(
            model_name='prettynum',
            name='price',
            field=models.IntegerField(null=True, verbose_name='价格'),
        ),
    ]