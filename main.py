# все объявления
# main class="vacancy-serp-content"
# h3 class="bloko-header-section-3"  все заголовки
# href="https://adsrv.hh.ru/click?b=921482&place=35&meta=xFoQeTZWlZWlzu0r_oqk-YnyamPwm33z_fx354W_S3v5i5XGOYoeDZP54HXYRO3GOP-uoMwoRP_orKgGxFtGftmTzBq2jjMY1CdvrGD_7ASdZ9xn4DK7yWEkaR_RP3aja_81dzxAS_sxD0kG1YOjBAdPr2c7VQrclAyHx6UjBi221WyClOIG7ncWemIgebEIDjLfyAi4SW948KCsrWUUQIsH7bkZiBT_C9p9Xdv03ITwyC0aMDiWYbbS-UKZBzXl-YH9WEV0QyBy655LKhB7eHuSFDubayu65JILzEdJ1puRoV0_muPlTe5MZxDjfxWMWHGdEu97bZC2KcAsooKrLChuksnjJ1kt6f-6eAEPQC89qoIb62N8PBmXrOoAVUIoEKQ_lxrn2G1z666SfOMC9XfZJFi2hBBJ3y_D7sEauBfe14XR_5nMIQ-QW26KCK9C46ziZQE4AUR5ts9vCGDQ60DZA4GVumXuPMdPZUl3RM9NhugGr8z6OVQPFAKharLGnSwQVry3YBfSnRso3Afz4w%3D%3D&clickType=link_to_vacancy"
# div class="bloko-text" для города
# div class="vacancy-description" текст вакансии для поиска слов "Django" и "Flask"
import json

import requests
from bs4 import BeautifulSoup
from fake_headers import Headers

def gen_headers():
    headers = Headers(browser='chrome', os='win')
    return headers.generate()

response = requests.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2', headers=gen_headers())

main_html = response.text
main_soup = BeautifulSoup(main_html, 'lxml')

vacancy_list_tag = main_soup.find('main', class_='vacancy-serp-content')
vacancy_tags = vacancy_list_tag.find_all('article')

vacancy_parsed = []

for vacancy_tag in vacancy_tags:
    h3_tag = vacancy_tag.find('h3', class_='bloko-header-section-3')
    a_tag = h3_tag.find('a')

    title = h3_tag.text.strip()
    link_relative = a_tag['href']
    link_absolut = f'https://spb.hh.ru{link_relative}'

    city_tag = vacancy_tag.find('div', class_='bloko-text')
    if 'Москва' in city_tag.text:
        need_city_tag = 'Москва'
    else:
        need_city_tag = 'Санкт-Петербург'

    response = requests.get(link_absolut)

    article_html = response.text
    article_soup = BeautifulSoup(article_html, 'lxml')

    description_tag = article_soup.find('div', class_='vacancy-description')
    description_text = description_tag.text.strip('')
    if "django" in str(description_text).lower() or 'flask' in str(description_text).lower():
        vacancy_dict = {
                'title': title,
                'link_absolut': link_absolut,
                'need_city_tag': need_city_tag,
                'description_text': description_text
            }

        vacancy_parsed.append(vacancy_dict)
        with open('vacancy_parsed.json', 'a', encoding='utf-8') as f:
            json.dump(vacancy_parsed, f, ensure_ascii=False, indent=2)
