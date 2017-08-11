import requests
from bs4 import BeautifulSoup
import os
import re


def ignore_everything_other_than_video(link):
    count = re.match('^/watch\?v=.+$', link)
    if count:
        return True
    else:
        return False


def formatting_views(views_string):
    return int(views_string.split()[0].replace(',', ''))


def scraper(content_of_page):
    ''' Change the line below if there's any discrepancy in scraping '''
    divisions = content_of_page.find_all('div', class_="yt-lockup-content")
    max_views = 0
    d = {}

    for division in divisions:
        watch_link = division.h3.a.get('href')
        if not ignore_everything_other_than_video(watch_link):
            continue

        try:
            views_as_string = division.div.next_sibling.ul.li.next_sibling.string
            views = formatting_views(views_as_string)
        except:
            continue

        if max_views > views:
            continue

        if max_views < views:
            max_views = views
            title = division.h3.a.get('title')
            d = {'title': title, 'link': watch_link, 'views': views}

    return d


def formatting(name):
    name = re.sub('[0-9"]', '', name).strip()
    name = re.sub('\t', '', name)
    return name


def change_dir():
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    return dname

def main():
    path_of_directory = change_dir()
    with open(os.path.join(path_of_directory, 'list')) as f:
        list_of_songs = f.readlines()

    songs_not_downloaded = []


    for song_name in list_of_songs:
        song_name = formatting(song_name)
        response = requests.get('https://www.youtube.com/results?', params={'search_query': song_name})
        content = BeautifulSoup(response.content, 'lxml')
        proper_video = scraper(content)
        if not proper_video:
            songs_not_downloaded.append(song_name)
            continue
        entire_link = "https://www.youtube.com{}".format(proper_video['link'])
        command = "youtube-dl -q --extract-audio --audio-format mp3 --xattrs --embed-thumbnail --audio-quality 0  -o '%(title)s.%(ext)s' '{}'".format(entire_link)
        os.system(command)
    
    if songs_not_downloaded:
        print('The following songs could not be downloaded: ')
        for index, song in enumerate(songs_not_downloaded):
            print('{}: {}'.format(index + 1, song))



if __name__ == '__main__':
    main()

