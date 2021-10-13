from django.db import models
from django.db.models.signals import pre_save
from myblog.utils import unique_slug_generator
from ckeditor.fields import RichTextField

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    # desc = models.TextField()
    desc = RichTextField(null=True, blank=True)
    author = models.CharField(max_length=20)
    title_tag = models.CharField(max_length=200, null=True, blank=True)
    post_image = models.ImageField(null=True, blank=True, upload_to="images/")
    post_date = models.DateTimeField(auto_now_add=True, blank=True)
    slug = models.SlugField(max_length=130, null=True, blank=True)

    def __str__(self):
        return self.title + 'by' + self.author

def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(slug_generator, sender=Post)


class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    message = models.TextField()
    timeStamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return 'Message from '+ self.name+'-'+ self.email

class Key(models.Model):
    ID = models.ForeignKey(Post, on_delete=models.CASCADE)

