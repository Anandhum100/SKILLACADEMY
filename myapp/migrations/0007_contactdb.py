# Generated by Django 4.2.3 on 2023-08-17 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='contactdb',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('NAME', models.CharField(blank=True, max_length=50, null=True)),
                ('EMAIL', models.CharField(blank=True, max_length=50, null=True)),
                ('MESSAGE', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
    ]
