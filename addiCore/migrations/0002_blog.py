# Generated by Django 2.2.6 on 2019-10-19 06:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('addiCore', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=100)),
                ('shortDescription', models.TextField()),
                ('content', models.TextField()),
                ('thumbnail', models.FileField(upload_to='')),
                ('image', models.FileField(upload_to='')),
                ('created_at', models.DateTimeField()),
                ('categories', models.CharField(max_length=100)),
                ('isDraft', models.BooleanField()),
                ('isPublished', models.BooleanField()),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
