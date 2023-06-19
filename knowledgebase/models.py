import os
from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils.deconstruct import deconstructible
from django.template.defaultfilters import filesizeformat
from django.core.validators import MinValueValidator
from django.db.models import Max

#from accounts.models import CustomUser

# Create your models here.

# new tables

# Clss to Validate Maximum File Upload Size
@deconstructible
class MaxSizeValidator:
    message = 'File size exceeds maximum allowed size of %(max_size)s.'
    code = 'max_size'

    def __init__(self, max_size):
        self.max_size = max_size
        super().__init__()

    def __call__(self, value):
        if value.size > self.max_size:
            raise ValidationError(
                self.message, code=self.code, params={'max_size': filesizeformat(self.max_size)}
            )





class OrganizationType(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    type_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.type_name

    class Meta:
        verbose_name_plural = "Organization Types"
        db_table = 'lkp_organization_types'
        ordering = ['id']   



class Organization(models.Model):
    id = models.AutoField(primary_key=True)
    sorting_order = models.SmallIntegerField(null=True, blank=True)
    organization_name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=50)
    mailing_address = models.CharField(max_length=200, blank=True)
    web_address = models.URLField(max_length=50, blank=True)
    organization_chief = models.CharField(max_length=100, blank=True)
    chief_designation = models.CharField(max_length=50, blank=True)
    focal_person = models.CharField(max_length=50, blank=True)
    fp_designation = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=100, blank=True)
    phone_no = models.CharField(max_length=20, blank=True)
    mobile_no = models.CharField(max_length=14, blank=True)
    logo = models.ImageField(upload_to='static/logo', blank=True)  
    organization_type = models.ForeignKey(OrganizationType, on_delete=models.PROTECT, null=True)

    def __str__(self) -> str:
        return self.organization_name

    class Meta:
        db_table = 'lkp_organizations'
        ordering = ['id']


class DataCommonCategory(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    category_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.category_name

    class Meta:
        db_table = 'lkp_data_common_categories'
        ordering = ['id']


class DataCategory(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    category_name = models.CharField(max_length=100)
    parent = models.PositiveSmallIntegerField(null=True)
    data_common_category = models.ForeignKey(DataCommonCategory, on_delete=models.PROTECT, null=True)
    #is_organizational_data = models.BooleanField(null=True)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, null=True)

    def __str__(self) -> str:
        return self.category_name

    class Meta:
        verbose_name_plural = "Data Categories"
        db_table = 'lkp_data_categories'
        ordering = ['id']


class DataAccessCategory(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    category_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.category_name

    class Meta:
        verbose_name_plural = "Data Access Categories"
        db_table = 'lkp_data_access_categories'
        ordering = ['id']
        

class DocumentApprovalStatus(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    approval_state = models.PositiveIntegerField(unique=True)
    approval_state_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.approval_state_name

    class Meta:
        db_table = 'lkp_document_approval_status'
        ordering = ['id']
        verbose_name_plural = 'Document Approval Status'


def get_upload_path(instance, filename):
    """Function to generate a new filename for uploaded files"""
    # Get the value of the property you want to use in the filename  
    #doc_id=len(Document.objects)==0 and 1 or Document.objects.order_by('id').first().id+1
    # doc_id = slugify(instance.title)
    #property_value = instance.id
    #new_name = f'{doc_id}-{name}{ext}'

    name, ext = os.path.splitext(filename)

    org_name = instance.organization.short_name
    doc_access_cat = instance.access_category.category_name
    doc_id = Document.objects.aggregate(Max('id'))['id__max']+1
    
    base_path = os.path.join('static', 'document', org_name, doc_access_cat)
    # path="static/documents/JRC/Public/doc_id.pdf"
    new_name = f'{doc_id}{ext}'
    return os.path.join(base_path, new_name)

def get_upload_path_thumb(instance, filename):
    """Function to generate a new filename for uploaded files"""
    name, ext = os.path.splitext(filename)

    org_name = instance.organization.short_name
    doc_access_cat = instance.access_category.category_name
    doc_id = Document.objects.aggregate(Max('id'))['id__max']+1
    
    base_path = os.path.join('static', 'document', org_name, doc_access_cat, 'thumbnail')
    # path="static/documents/JRC/Public/document.pdf"
    new_name = f'thumb_{doc_id}{ext}'
    return os.path.join(base_path, new_name)

def get_document_file_upload_path(instance, filename):
    """Function to generate a new filename for uploaded files"""
    name, ext = os.path.splitext(filename)
    # file_id = DocumentFile.objects.aggregate(Max('id'))['id__max']
    # if file_id == None:
    #       file_id = 1
    # else:
    #       file_id = file_id + 1 
    
    org_name = instance.document.organization.short_name
    doc_access_cat = instance.document.access_category.category_name
    doc_id = instance.document.id

    base_path = os.path.join('static','document', org_name, doc_access_cat)    
    
    existing_files = DocumentFile.objects.filter(document__id=instance.document.id).count()
    new_name = f'{doc_id}_{existing_files+1}{ext}'

    # path_example ="static/document/JRC/Public/filename_no_of_doc_doc_id.pdf"
    return os.path.join(base_path, new_name)


class Document(models.Model):
    # id = models.AutoField(primary_key=True)
    id = models.PositiveIntegerField(primary_key=True)
    

    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, null=True)

    data_category = models.ForeignKey(DataCategory, on_delete=models.PROTECT, null=True, verbose_name='Data Category')

    # sub_category_id = models.ForeignKey("SubCategory", on_delete=models.PROTECT, null=True)
    # sub_sub_category_id = models.ForeignKey("SubSubCategory", on_delete=models.PROTECT, null=True)
    # org_category_id = models.ForeignKey("OrgCategory", on_delete=models.PROTECT, null=True)
    # org_sub_category_id = models.ForeignKey("OrgSubCategory", on_delete=models.PROTECT, null=True)
    # org_sub_sub_category_id = models.ForeignKey("OrgSubSubCategory", on_delete=models.PROTECT, null=True)

    title = models.CharField(max_length=500)
    subject = models.CharField(max_length=500, blank=True)
    description = models.TextField(null=True, blank=True)
    author = models.CharField(max_length=100, blank=True)
    access_category = models.ForeignKey(
        DataAccessCategory, on_delete=models.PROTECT, null=True, verbose_name='Access Category')
    # publication_date = models.CharField(max_length=50, null=True, blank=True)
    publication_date = models.DateField(null=True, blank=True, verbose_name='Publication Date')

    # file_name = models.FileField(
    #     upload_to='static/document', max_length=500, null=True, blank=True)
    # thumbnail = models.ImageField(
    #     upload_to='static/img', null=True, blank=True)
    
    file_name = models.FileField(upload_to=get_upload_path, max_length=500, null=True, blank=True)
    thumbnail = models.ImageField(upload_to=get_upload_path_thumb, null=True, blank=True, verbose_name='Upload Thumbnail')

    keywords = models.CharField(max_length=1000, null=True, blank=True)
    entry_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    entry_by = models.CharField(max_length=100, null=True, blank=True, verbose_name='Entry By')
    #entry_by = models.ForeignKey(CustomUser, null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    modified_by = models.CharField(max_length=100, null=True, blank=True, verbose_name='Modify By')
    document_approval_status = models.ForeignKey(DocumentApprovalStatus, on_delete=models.PROTECT, null=True, 
                                                 verbose_name= 'Approval Status', to_field='approval_state', default=1)
    is_parent_available = models.BooleanField(null=True, blank=True)
    parent_id = models.PositiveBigIntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        db_table = 'tbl_documents'
        ordering = ['id']


class DocumentFile(models.Model):
    #  id = models.AutoField(primary_key=True)
     id = models.PositiveIntegerField(primary_key=True)
     file = models.FileField(upload_to=get_document_file_upload_path, max_length=500, null=False, verbose_name= 'Select File (Maximum 25MB)', 
                                  validators=[FileExtensionValidator(allowed_extensions= ['pdf']), MaxSizeValidator(25 * 1024 * 1024),])
     uploaded_at = models.DateTimeField(auto_now_add=True)
     document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='doc_files')
    


     def __str__(self) -> str:
          return self.file.name
     
     class Meta:
          db_table = 'tbl_document_files'
          ordering = ['id']
          verbose_name = 'Upload Document'

class ArticleDetail(models.Model):
    id = models.AutoField(primary_key=True)

    organization = models.ForeignKey(
        Organization, on_delete=models.PROTECT, null=True, blank=True)
    data_category = models.ForeignKey(
        DataCategory, on_delete=models.PROTECT, null=True, blank=True)
    title = models.CharField(max_length=500)
    subject = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    author = models.CharField(max_length=100, null=True, blank=True)
    access_category = models.ForeignKey(
        DataAccessCategory, on_delete=models.PROTECT, null=True, blank=True)
    publication_date = models.CharField(max_length=50, null=True, blank=True)
    file_name = models.FileField(
        upload_to='static/article', null=True, blank=True)
    thumbnail = models.ImageField(
        upload_to='static/img', null=True, blank=True)
    is_published = models.BooleanField(null=True, blank=True)
    source = models.CharField(max_length=500, null=True, blank=True)
    keywords = models.CharField(max_length=1000, null=True, blank=True)
    entry_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    #entry_by = models.ForeignKey(CustomUser, null=True, blank=True)
    entry_by = models.CharField(max_length=100, null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    modified_by = models.CharField(max_length=100, null=True, blank=True)
    is_parent_available = models.BooleanField(null=True, blank=True)
    parent_id = models.PositiveBigIntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        db_table = 'tbl_article_details'
        ordering = ['id']


class ArticleDocDetail(models.Model):
    id = models.AutoField(primary_key=True)
    article_detail = models.ForeignKey(
        ArticleDetail, on_delete=models.PROTECT, null=True)
    document = models.ForeignKey(
        Document, on_delete=models.PROTECT, null=True)

    def __str__(self) -> str:
        return self.article_id

    class Meta:
        db_table = 'tbl_article_doc_details'
        ordering = ['id']


class ImportantLinkCategory(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    category_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.category_name

    class Meta:
        db_table = 'lkp_important_link_categories'
        ordering = ['id']


class ImportantLink(models.Model):
    id = models.AutoField(primary_key=True)
    link_category = models.ForeignKey(
        ImportantLinkCategory, on_delete=models.PROTECT, null=True, blank=True)
    title = models.CharField(max_length=500, null=True, blank=True)
    web_link = models.CharField(max_length=255)
    description = models.CharField(max_length=500, null=True, blank=True)
    entry_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    entry_by = models.CharField(max_length=100, null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    modified_by = models.CharField(max_length=100, null=True, blank=True)
    delete_status = models.BooleanField(null=True, blank=True)

    def __str__(self) -> str:
        return self.link_category

    class Meta:
        db_table = 'tbl_important_links'
        ordering = ['id']

# database tables


class ArticleCategory(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    category_name = models.CharField(max_length=100)
    logo_name = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self) -> str:
        return self.category_name

    class Meta:
        verbose_name_plural = "Article Categories"
        db_table = 'kbase_article_categories'
        ordering = ['id']


class ArticlePublishCategory(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    category_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.category_name

    class Meta:
        verbose_name_plural = "Article Publish Categories"
        db_table = 'kbase_article_pub_categories'
        ordering = ['id']


class Article(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    parent_id = models.SmallIntegerField(
        null=True, validators=[MinValueValidator(0)])

    article_category = models.ForeignKey(
        ArticleCategory, on_delete=models.PROTECT, null=True)
    publish_category = models.ForeignKey(
        ArticlePublishCategory, on_delete=models.PROTECT)
    #entry_by = models.ForeignKey(CustomUser, null=True, blank=True)
    entry_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)

    def __str__(self) -> str:
        return self.title

    # def get_article_category_name(self):
    #     return self.article_category.category_name
    # get_article_category_name.short_description = 'Article Category Name'
    # get_article_category_name.admin_order_field = 'article_category__category_name'

    class Meta:
        db_table = 'kbase_articles'
        ordering = ['id']
