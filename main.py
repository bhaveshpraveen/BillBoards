import requests
from bs4 import BeautifulSoup
import os
import re
import json


def ignore_everything_other_than_video(link):
    count = re.match('^/watch\?v=.+$', link)
    if count:
        return True
    else:
        return False


# def extract_view_count_from_url(url):
#     data_object = os.popen('youtube-dl -J "{}"'.format(url))
#     data = data_object.readline()
#     data_dictionary = json.loads(data)
#     ''' If view_count not present, default to None '''
#     return data_dictionary.get('view_count', None)


def formatting_views(views_string):
    return int(views_string.split()[0].replace(',', ''))


def scraper(content_of_page):
    ''' Change the line below for discrepancies in scraping '''
    divisions = content_of_page.find_all('div', class_="yt-lockup-content")
    # print(divisions)
    max_views = 0
    d = {}
    # links = [header.a.get('href') if ignore_everything_other_than_video(header.a.get('href')) for header in necessary_headers]
    for division in divisions:
        watch_link = division.h3.a.get('href')
        if not ignore_everything_other_than_video(watch_link):
            continue

        try:
            views_as_string = division.div.next_sibling.ul.li.next_sibling.string
            views = formatting_views(views_as_string)
        except:
            continue

        # print(watch_link)

        if max_views > views:
            continue

        if max_views < views:
            max_views = views
            title = division.h3.a.get('title')
            d = {'title': title, 'link': watch_link, 'views': views}

    return d


# directory_to_download_in = '/media/ichigo/Seagate Backup Plus Drive/BHAVESH/'
# os.chdir(directory_to_download_in)
# # os.mkdir('Billboards')
# os.chdir('Billboards')


def formatting(name):
    name = re.sub('[0-9"]', '', name).strip()
    name = re.sub('\t', '', name)
    return name


def change_dir():
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    return dname

path_of_directory = change_dir()
with open(os.path.join(path_of_directory, 'list')) as f:
    list_of_songs = f.readlines()

songs_not_downloaded = []


for song_name in list_of_songs:
    song_name = formatting(song_name)
    response = requests.get('https://www.youtube.com/results?', params={'search_query': song_name})
    content = BeautifulSoup(response.content)
    proper_video = scraper(content)
    if not proper_video:
        songs_not_downloaded.append(song_name)
        continue
    print(proper_video)
    # os.system("youtube-dl --extract-audio --audio-format mp3 -o '%(title)s.%(ext)s' {}".format(proper_video['watch_link']))

    # print(links)
    # max_views = 0
    # dictionary_with_views = {}
    # for link in links:
    #     entire_link = 'https://www.youtube.com{}'.format(link)
    #     views = extract_view_count_from_url(entire_link)
    #     if not views:
    #         continue
    #     dictionary_with_views[views] = entire_link
    #     if max_views < views:
    #         max_views = views
    # print(entire_link, dictionary_with_views)
    # link_to_download = dictionary_with_views[max_views]
    # print(link_to_download)
    # os.system("youtube-dl --extract-audio --audio-format mp3 {}".format(link_to_download))

    # video_list = soup.find_all('a', class_=' yt-uix-sessionlink      spf-link ')

    # for i in video_list:
    #     link = i.get('href')
    #     print(link)
    #     if link:
    #         first_part = 'https://www.youtube.com'
    #         entire_link = first_part + link
    #         os.system("youtube-dl --extract-audio --audio-format mp3 {}".format(entire_link))
    #         break
