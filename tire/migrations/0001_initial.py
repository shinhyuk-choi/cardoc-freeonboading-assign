# Generated by Django 3.2.9 on 2021-11-26 05:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trim_id', models.IntegerField(help_text='자동차 정보 조회 API의 trimId', unique=True)),
                ('f_width', models.CharField(help_text='앞바퀴 단면폭', max_length=10)),
                ('f_profile', models.CharField(help_text='앞바퀴 편평비', max_length=10)),
                ('f_diameter', models.CharField(help_text='앞바퀴 림직경', max_length=10)),
                ('r_width', models.CharField(help_text='뒷바퀴 단면폭', max_length=10)),
                ('r_profile', models.CharField(help_text='뒷바퀴 편평비', max_length=10)),
                ('r_diameter', models.CharField(help_text='뒷바퀴 림직경', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserTire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('tire', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_tires', to='tire.tire', to_field='trim_id')),
            ],
        ),
    ]
