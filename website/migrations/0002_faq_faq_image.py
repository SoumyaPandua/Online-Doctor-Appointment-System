# Generated by Django 5.0.4 on 2024-08-26 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='faq',
            name='faq_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
