import requests
import codecs
from bs4 import BeautifulSoup as Bs
from random import randint

__all__=('staffam',)
headers=[{"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5)AppleWebKit/605.1.15 (KHTML, like Gecko)Version/12.1.1 Safari/605.1.15",
         "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"},
         {'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
          "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"},
         {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
          "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}]


def staffam(url,city=None,language=None):
    domain = "https://staff.am"
    errors = []
    jobs = []
    if url:
        resp = requests.get(url,headers=headers[randint(0,2)])
        if resp.status_code == 200:
            soup = Bs(resp.content, 'html.parser')
            main_div = soup.find('div', id='w0')
            if not main_div.find('div',attrs={'class':'empty'}):
                all_div = main_div.find_all('div', attrs={'data-key': True})
                for div in all_div:
                    href = div.find('a', attrs={'data-pjax': 0, 'class': False})['href']
                    title = div.find('p', attrs={'class': 'font_bold'}).text
                    company = div.find('p', attrs={'class': 'job_list_company_title'}).text
                    logo=div.find('img')['src']
                    deadline=div.find('span',attrs={'class':"formatted_date"}).text

                    jobs.append({'title': title, 'url': domain + href,
                                 'logo': logo,
                                 'company': company,
                                 'city_id': city,
                                 'language_id': language,
                                 "deadline":deadline
                                 })
                    print("parsed")
            else:
                errors.append({'url': url, "title": "Div does not exists"})
        else:
            errors.append({'url': url, "title": "Page Not Response"})

    return jobs,errors



if __name__ == '__main__':
    url='https://staff.am/en/jobs/categories/index?JobsFilter%5Bkey_word%5D=python#search_list_block'
    jobs,errors=staffam(url)
    h=codecs.open('../work_d.txt', 'w', 'utf-8')
    h.write(str(jobs))
    h.close()
    print(errors)
