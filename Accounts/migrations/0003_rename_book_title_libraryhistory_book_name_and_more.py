# Generated by Django 5.1.1 on 2024-12-18 04:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0002_alter_feeshistory_amount_paid_alter_user_role'),
    ]

    operations = [
        migrations.RenameField(
            model_name='libraryhistory',
            old_name='book_title',
            new_name='book_name',
        ),
        migrations.RenameField(
            model_name='libraryhistory',
            old_name='borrowed_date',
            new_name='borrow_date',
        ),
    ]
