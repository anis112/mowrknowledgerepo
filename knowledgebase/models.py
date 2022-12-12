from django.db import models
from django.core.validators import MinValueValidator
#from accounts.models import CustomUser

# Create your models here.

# new tables


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
    logo = models.ImageField(
        upload_to='static/logo', blank=True)

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
    data_common_category = models.ForeignKey(
        DataCommonCategory, on_delete=models.PROTECT, null=True)
    #is_organizational_data = models.BooleanField(null=True)
    organization = models.ForeignKey(
        Organization, on_delete=models.PROTECT, null=True)

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


class Document(models.Model):
    id = models.AutoField(primary_key=True)
    #id = models.PositiveSmallIntegerField(primary_key=True)

    organization = models.ForeignKey(
        Organization, on_delete=models.PROTECT, null=True)

    data_category = models.ForeignKey(
        DataCategory, on_delete=models.PROTECT, null=True)

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
        DataAccessCategory, on_delete=models.PROTECT, null=True)
    publication_date = models.CharField(max_length=50, null=True, blank=True)

    file_name = models.FileField(
        upload_to='static/document', max_length=500, null=True, blank=True)
    thumbnail = models.ImageField(
        upload_to='static/img', null=True, blank=True)

    keywords = models.CharField(max_length=1000, null=True, blank=True)
    entry_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    entry_by = models.CharField(max_length=100, null=True, blank=True)
    #entry_by = models.ForeignKey(CustomUser, null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    modified_by = models.CharField(max_length=100, null=True, blank=True)

    is_parent_available = models.BooleanField(null=True, blank=True)
    parent_id = models.PositiveBigIntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        db_table = 'tbl_documents'
        ordering = ['id']


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
