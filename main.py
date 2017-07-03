import requests
from bs4 import BeautifulSoup
import os
import re

directory_to_download_in = '/media/ichigo/Seagate Backup Plus Drive/BHAVESH/'
os.chdir(directory_to_download_in)
# os.mkdir('Billboards')
os.chdir('Billboards')


def formatting(name):
    name = re.sub('[0-9"]', '', name).strip()
    name = re.sub('\t', '', name)
    return name

with open('/home/ichigo/Desktop/billboards/list') as f:
    list_of_songs = f.readlines()

for song_name in list_of_songs:
    song_name = formatting(song_name)
    response = requests.get('https://www.youtube.com/results?', params={'search_query': song_name})
    soup = BeautifulSoup(response.content)
    ''' Change the below line alone'''
    video_list = soup.find_all('a', class_=' yt-uix-sessionlink      spf-link ')

    for i in video_list:
        link = i.get('href')
        print(link)
        if link:
            first_part = 'https://www.youtube.com'
            entire_link = first_part + link
            os.system("youtube-dl --extract-audio --audio-format mp3 {}".format(entire_link))
            break
