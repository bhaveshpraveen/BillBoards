import requests
from bs4 import BeautifulSoup
import os
import re
import json


def ignore_everything_other_than_video(link):
    count = re.match('^/watch?v=', link)
    if count == 9:
        return True
    else:
        return False


def extract_view_count_from_url(url):
    data = os.popen('youtube-dl -J "{}"'.format(url))
    data = data.readlines()
    data = json.loads(data)
    return data['view_count']


def scraper(content_of_page):
    necessary_headers = content_of_page.find_all('h3', class_="yt-lockup-title ")
    links = [header.a.get('href') if ignore_everything_other_than_video(header.a.get('href')) for header in necessary_headers]
    links = []
    for header in necessary_headers:
        watch_link = header.a.get('href')
        if ignore_everything_other_than_video(watch_link):
            links.append(watch_link)
    return links


# directory_to_download_in = '/media/ichigo/Seagate Backup Plus Drive/BHAVESH/'
# os.chdir(directory_to_download_in)
# # os.mkdir('Billboards')
# os.chdir('Billboards')


def formatting(name):
    name = re.sub('[0-9"]', '', name).strip()
    name = re.sub('\t', '', name)
    return name

with open('/home/ichigo/Desktop/billboards/list') as f:
    list_of_songs = f.readlines()

for song_name in list_of_songs:
    song_name = formatting(song_name)
    response = requests.get('https://www.youtube.com/results?', params={'search_query': song_name})
    content = BeautifulSoup(response.content)
    ''' Change the below line alone'''
    links = scraper(content)

    max_views = 0
    dictionary_with_views = {}
    for link in links:
        entire_link = 'https://www.youtube.com{}'.format(link)
        views = extract_view_count_from_url(entire_link)
        dictionary_with_views[views] = entire_link
        if max_views < views:
            max_views = views
    os.system("youtube-dl --extract-audio --audio-format mp3 {}".format(entire_link))

    # video_list = soup.find_all('a', class_=' yt-uix-sessionlink      spf-link ')

    # for i in video_list:
    #     link = i.get('href')
    #     print(link)
    #     if link:
    #         first_part = 'https://www.youtube.com'
    #         entire_link = first_part + link
    #         os.system("youtube-dl --extract-audio --audio-format mp3 {}".format(entire_link))
    #         break
