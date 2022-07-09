from django.contrib import admin
from .models import City,Language,Vacancy,Error,Url

admin.site.register(City)
admin.site.register(Language)
admin.site.register(Error)
admin.site.register(Url)

class VacancyAdmin(admin.ModelAdmin):
    ist_display = ('id', 'title', 'language', 'city', 'timestamp')
    list_display_links = ('id', 'title')
    search_fields = ('title','language', 'city',)

admin.site.register(Vacancy,VacancyAdmin)
