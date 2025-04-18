# Generated by Django 4.2 on 2025-03-30 02:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('erp', '0002_alter_category_id_alter_client_id_alter_detsale_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='date_creation',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='date_updated',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='category',
            name='user_updated',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_updated', to=settings.AUTH_USER_MODEL),
        ),
    ]
