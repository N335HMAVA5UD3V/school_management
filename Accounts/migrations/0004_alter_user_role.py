# Generated by Django 5.1.1 on 2024-12-25 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0003_rename_book_title_libraryhistory_book_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('ADMIN', 'Admin'), ('STAFF', 'Office Staff'), ('LIBRARIAN', 'Librarian')], default='ADMIN', max_length=20),
        ),
    ]
