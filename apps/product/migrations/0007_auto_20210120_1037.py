# Generated by Django 3.1.4 on 2021-01-20 04:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_remove_productimage_alt_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='body',
            new_name='description',
        ),
    ]
