# encoding=utf-8

import urllib
import json
import io
from BeautifulSoup import BeautifulSoup


URL = 'https://www.kinopoisk.ru/film/435/'


def parse_url(url):
    data = urllib.urlopen(url)
    data = data.read().decode("windows-1251").encode("utf-8")
    soup = BeautifulSoup(''.join(data))

    parsed_data = dict({'year': 0, 'genres':[], 'country': '', 'budget': 0, 'usa': 0, 'world': 0, 'age_restriction': 0,
                        'duration': 0, 'rating': 0})

    content = soup.body.find('div', id='infoTable').findAll('td')
    for i in range(len(content)):
        if content[i].contents[0].string == u'год':
            parsed_data['year'] = content[i + 1].text
        if content[i].contents[0].string == u'страна':
            parsed_data['country'] = content[i + 1].text
        if content[i].contents[0].string == u'бюджет':
            parsed_data['budget'] = content[i + 1].find('div').text.replace('&nbsp;', '').replace(u'сборы', '')
        if content[i].contents[0].string == u'сборы в США':
            parsed_data['usa'] = content[i + 1].find('div').text.replace('&nbsp;', '').replace(u'сборы', '')
        if content[i].contents[0].string == u'сборы в мире':
            parsed_data['world'] = content[i + 1].find('div').text.replace('&nbsp;', '').replace(u'сборы', '')
        if content[i].contents[0].string == u'возраст':
            parsed_data['age_restriction'] = content[i + 1].text
        if content[i].contents[0].string == u'время':
            parsed_data['duration'] = content[i + 1].contents[0].string

    content = soup.find('div', id='block_rating', itemprop='aggregateRating').find('a')
    parsed_data['rating'] = content.find('span').string

    for genre in soup.find('span', itemprop="genre").findAll('a'):
        parsed_data['genres'].append(genre.string)

    return parsed_data


with io.open('film_info', 'w', encoding='utf-8') as film:
    parsed = parse_url(URL)
    # print(parsed['country'])
    film.write(json.dumps(parsed, indent=4, sort_keys=True, ensure_ascii=False))

    film.close()
