import os,sys
project=os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(project)
os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping_service.settings'
import django
django.setup()
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from scraping.models import Vacancy,Error,Url
from  scraping_service.settings import EMAIL_HOST_USER
import datetime
today=datetime.date.today()

admin_email=EMAIL_HOST_USER
subject=f"All available jobs for {today}"
text_content="Our service"
from_email=EMAIL_HOST_USER

empty="<h2>Unfortunately there is no new jobs today(</h2>"
User=get_user_model()
qs = User.objects.filter(send_email=True).values('city','language','email')
users_dict={}
for i in qs:
    users_dict.setdefault((i['city'], i['language']), [])
    users_dict[(i['city'],i['language'])].append(i['email'])
if users_dict:
    params={'city_id__in':[],'language_id__in':[]}
    for pairs in users_dict.keys():
        params['city_id__in'].append(pairs[0])
        params['language_id__in'].append(pairs[1])
    qs=Vacancy.objects.filter(**params,timestamp=today).values()[:15]
    vacancies={}
    for i in qs:
        vacancies.setdefault((i['city_id'], i['language_id']),[])
        vacancies[(i['city_id'], i['language_id'])].append(i)
    for keys,emails in users_dict.items():
        rows=vacancies.get(keys,[])
        html=""
        if len(rows)>0:
            html+="<h2 align='center' style='color: darkgreen'> Your job alert for today</h2><br><br>"
        for row in rows:
            if row['logo']=="https://hirebee-main-new.s3.amazonaws.com/staff.am/images/background/company_default_image.svg":
                tm_logo="https://cdn3.vectorstock.com/i/1000x1000/37/07/not-available-sign-or-stamp-vector-22523707.jpg"
            else:
                tm_logo=row['logo']
            html += f"""
            
                <div class="tab-content col-md-12" 
                style="	 width: 700px;
                height: auto;
                  margin: auto;
            
                background-color: #ffffff;
                    color: #039;
                  ">
                         <h3 class="card-header"><a style="text-decoration:none; " href="{row['url']}"> {row['title']} </a></h3>
                         <div class="card-body">
                           <p style="color: darkgreen" class="card-title" align="center">Company - {row['company']}</p>
                             <img height="100" width="100" src="{tm_logo}" alt="Card image cap">
                             <p align="right" class="card-text" style="color: crimson">Deadline / {row['deadline']}</p>
                              </div>
                              <hr>
                               """

        _html = html if html else empty
        for email in emails:
            to = email
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(_html, "text/html")
            msg.send()

    # sending daily errors to site admin
    qs = Error.objects.filter(timestamp=today)
    text_content = ""
    subject = ""
    to = admin_email
    content = ""
    if qs.exists():
        error = qs.first()
        data = error.data.get('errors', [])
        for i in data:
            content += f'<p"><a href="{i["url"]}">Error: {i["title"]}</a></p><br>'
        subject = "Scraping errors"
        text_content = f"For {today}"
        from_email = EMAIL_HOST_USER
        data = error.data.get('user_data')
        if data:
            content += '<hr>'
            content += '<h2>Users Requests</h2>'
            for i in data:
                content += f"<h4> City{i['city']}',<br> language {i['language']} <br> email {i['email']}     </h4>"
            subject = "User Requests"
            text_content = f"For {today}"
            from_email = EMAIL_HOST_USER

    # missing urls for language and city
    qs = Url.objects.all().values('city', 'language')
    urls_dict = {(i['city'], i['language']): True for i in qs}
    url_err = ""
    for keys in users_dict.keys():
        if keys not in urls_dict:
            if keys[0] and keys[1]:
                url_err = f"<h4>For this city{keys[0]} and  language {keys[1]} not URL</h4>"
    if url_err:
        subject += "Missing Urls"
        content += url_err
    if subject:
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(content, "text/html")
        msg.send()