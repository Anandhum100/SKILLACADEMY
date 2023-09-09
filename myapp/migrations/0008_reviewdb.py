# Generated by Django 4.2.3 on 2023-08-17 10:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0007_contactdb'),
    ]

    operations = [
        migrations.CreateModel(
            name='reviewdb',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('selectcourse', models.CharField(blank=True, max_length=50, null=True)),
                ('Userphoto', models.ImageField(null=True, upload_to='Media/user_img')),
                ('Review', models.TextField()),
                ('User', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
