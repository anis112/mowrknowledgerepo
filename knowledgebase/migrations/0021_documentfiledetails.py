# Generated by Django 4.1 on 2023-06-11 06:44

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import knowledgebase.models


class Migration(migrations.Migration):

    dependencies = [
        ('knowledgebase', '0020_alter_articledocdetail_document_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentFileDetails',
            fields=[
                ('id', models.PositiveBigIntegerField(primary_key=True, serialize=False)),
                ('file', models.FileField(max_length=500, upload_to=knowledgebase.models.get_document_file_upload_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf']), knowledgebase.models.MaxSizeValidator(26214400)], verbose_name='Select File (Maximum 25MB)')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doc_file_details', to='knowledgebase.document')),
            ],
            options={
                'verbose_name': 'Upload Document',
                'db_table': 'tbl_document_file_details',
                'ordering': ['id'],
            },
        ),
    ]
