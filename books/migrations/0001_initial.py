# Generated by Django 5.2.1 on 2025-05-17 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='book_images/')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('stock', models.PositiveIntegerField(default=0)),
                ('book_type', models.CharField(choices=[('sell', 'For Sale'), ('borrow', 'For Borrowing'), ('both', 'For Sale & Borrowing')], default='sell', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
