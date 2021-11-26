# Generated by Django 3.2.9 on 2021-11-26 05:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tire', '0002_usertire_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertire',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_tires', to=settings.AUTH_USER_MODEL, to_field='id'),
        ),
    ]
