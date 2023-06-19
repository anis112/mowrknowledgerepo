# Generated by Django 4.1 on 2023-06-05 04:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('knowledgebase', '0016_alter_documentfile_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articledocdetail',
            name='document',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='knowledgebase.documentdetail'),
        ),
        migrations.DeleteModel(
            name='Document',
        ),
    ]