# Generated by Django 4.1 on 2022-10-24 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('knowledgebase', '0002_alter_articledetail_access_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articledetail',
            name='publication_date',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='publication_date',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
