# Generated by Django 5.2.3 on 2025-07-07 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_other_price_alter_other_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='other',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='Other_images/'),
        ),
        migrations.AlterField(
            model_name='other',
            name='price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
