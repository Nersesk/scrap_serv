from django.db import models
from .utils import make_slug
from jsonfield import JSONField
def default_urls():
    return {'work':'',"staff":'','dou':''}


class City(models.Model):
    name = models.CharField(max_length=50,unique=True,
                            verbose_name="Name of City")
    slug=models.SlugField(max_length=50,blank=True,
                          verbose_name="Slug",unique=True)

    def __str__(self):
        return f"{self.name}"
    class Meta:
        verbose_name='City'
        verbose_name_plural="Cities"

class Language(models.Model):
    name = models.CharField(max_length=50, unique=True,
                           verbose_name="Name of Programing Language")
    slug = models.SlugField(max_length=50, blank=True,
                            verbose_name="Slug", unique=True)

    def __str__(self):
        return f"{self.name}"
    class Meta:
        verbose_name='Programing language'
        verbose_name_plural="Programing languages"

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug=make_slug(self.name)
        super().save(*args,**kwargs)

class Vacancy(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=250,verbose_name="Job Title")
    company = models.CharField(max_length=250,verbose_name="Company name")
    logo = models.CharField(verbose_name="image",null=True,max_length=200)
    deadline=models.CharField(max_length=50,null=True,default="")
    city=models.ForeignKey(City,on_delete=models.CASCADE,verbose_name="City of job")
    language = models.ForeignKey(Language, on_delete=models.CASCADE,verbose_name="Language of programming")
    timestamp = models.DateField(auto_now_add=True)


    def __str__(self):
        return f"{self.title}"
    class Meta:
        verbose_name='Vacancy'
        verbose_name_plural="Vacancies"
        ordering=('-timestamp',)

class Error(models.Model):
    timestamp = models.DateField(auto_now_add=True)
    data=models.JSONField()

    def __str__(self):
        return f'{self.timestamp}'

class Url(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="City of job")
    language = models.ForeignKey(Language, on_delete=models.CASCADE, verbose_name="Language of programming")
    url_data=JSONField(default=default_urls)

    class Meta:
        unique_together=('city','language')