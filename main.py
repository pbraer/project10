from urllib.request import urlopen
from bs4 import BeautifulSoup


def html_make(url):
    html = urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")
    for script in soup(["script", "style"]):
        script.extract()
    text = soup.get_text()
    text = text[text.find('Жанр по версии IMDb') + len('Жанр по версии IMDb'):text.find('По режиссёрам[править | править код]')]
    return text


def info_make(html):
    text_elements = html.split('\n')
    films = {}
    genres = []
    info = []
    step = 0
    for element in text_elements:
        if element != '' and (len(element) >= 4 or element.isdigit() == False):
            step += 1
            if element == 'Супергеройский боевикфантастика':
                element = 'Супергеройский боевик, фантастика'
            if step == 1:
                name = element
            elif step == 2:
                info.append(element)
            elif step == 4:
                if element.find(', ') != -1:
                    element = element.split(', ')
                    for elem in element:
                        if elem not in genres:
                            genres.append(elem)
                    info.append(element)
                else:
                    if element not in genres:
                        genres.append(element)
                    el = [element]
                    info.append(el)
                films[name] = info
                info = []
                step = 0
    return films


def genres_make(html_jan):
    text_elements = html_jan.split('\n')
    genres = []
    step = 0
    for element in text_elements:
        if element != '' and (len(element) >= 4 or element.isdigit() == False):
            step += 1
            if step == 4:
                if element == 'Супергеройский боевикфантастика':
                    element = 'Супергеройский боевик, фантастика'
                if element.find(', ') != -1:
                    element = element.split(', ')
                    for elem in element:
                        if elem not in genres:
                            genres.append(elem)
                else:
                    if element not in genres:
                        genres.append(element)
                step = 0
    return genres


def choose(genres):
    print('Выберите жанр фильма:')
    num_genres = {}
    for i in range(0, len(genres)):
        print((i+1), ' ', genres[i], sep='')
        num_genres[str(i+1)] = genres[i]
    chosen = input()
    print()
    return num_genres[chosen]


def out(all_films, chosen):
    number = 0
    for film in all_films:
        info = all_films[film]
        if chosen in info[1]:
            print()
            number += 1
            print(number, '. ', film, ', ', info[0], sep='')
            for gen in info[1]:
                print(gen, ' ', sep='', end='')
            print()


html_text = html_make('https://ru.wikipedia.org/wiki/250_%D0%BB%D1%83%D1%87%D1%88%D0%B8%D1%85_%D1%84%D0%B8%D0%BB%D1%8C%D0%BC%D0%BE%D0%B2_%D0%BF%D0%BE_%D0%B2%D0%B5%D1%80%D1%81%D0%B8%D0%B8_IMDb')
films = info_make(html_text)
genre = genres_make(html_text)
choice = choose(genre)
out(films, choice)
