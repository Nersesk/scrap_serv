import datetime
import os,sys

project=os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(project)
os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping_service.settings'
import django
django.setup()


from scraping.parser import *
from scraping.models import City, Vacancy, Language, Error, Url
from django.db import DatabaseError
from django.contrib.auth import get_user_model


User=get_user_model()

#all users whom we need to send emails
def get_settings():
    qs=User.objects.filter(send_email=True).values()
    settings_set=set((q['city_id'],q['language_id']) for q in qs)
    return settings_set


def get_urls(_settings):
    qs=Url.objects.all().values()
    url_dict={(q['city_id'],q['language_id']):q["url_data"] for q in qs}
    urls=[]
    for pair in _settings:
        if pair in url_dict:
            tmp={}
            tmp['city']=pair[0]
            tmp['language']=pair[1]
            tmp['url_data']=url_dict[pair]
            urls.append(tmp)
    return urls
settings=get_settings()
url_list = get_urls(settings)

parsers=((staffam,"staff"),)


jobs,errors=[],[]


for data in url_list:
    for func,key in parsers:
        try:
            url=data['url_data'][key]
            j, i = func(url,city=data['city'],language=data['language'])
            jobs+=j
            errors+=i
        except KeyError:
            pass

for job in jobs:
    try:
        v=Vacancy(**job)
        v.save()
    except DatabaseError:
        pass
if errors:
    qs=Error.objects.filter(timestamp=datetime.datetime.today())
    if qs.exists():
        err=qs.first()
        print(type(err.data))
        err.data.update({'errors':errors})
        err.save()
    else:
        Error(data={'errors':errors}).save()

# h=codecs.open('../work_d.txt', 'w', 'utf-8')
# h.write(str(jobs))
# h.close()


ten_days=datetime.datetime.today()-datetime.timedelta(10)
Vacancy.objects.filter(timestamp__lte=ten_days).delete()
