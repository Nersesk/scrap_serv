from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from .forms import FindForm
from .models import Vacancy

def home_view(request):
    form=FindForm()
    return render(request, "scraping/home.html", {'form':form})

def list_view(request):
    form=FindForm()
    city = request.GET.get('city')
    language = request.GET.get('language')
    context={'city':city,'language':language}
    query_set=[]
    _filter = {}
    if city or language:
        if city:
            _filter['city__slug'] = city
        if language:
            _filter['language__slug'] = language
    query_set = Vacancy.objects.filter(**_filter)
    if query_set:
        paginator = Paginator(query_set, 15)  # Show 15 jobs per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context["object_list"] =page_obj
    context['form']=form
    return render(request, "scraping/list.html", context)

