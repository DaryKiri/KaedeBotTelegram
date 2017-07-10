import requests, json
import random as rnd_gen

playlists_id = ['PLLQmKWavSS8HJysQrJHkCeW1IZNX55mv3', 'PLLQmKWavSS8FcHulKE1Xe2-AsdCSrsq_D']
url = 'https://www.googleapis.com/youtube/v3/playlistItems'
source_url = "https://www.youtube.com/watch"
key = ''
result_count = 15

def get_video(page=None):
    """
    Retrieves a number of random videos from from the youtube playlist

    returns {'nextPageToken': token, 'prevPageToken': token, 'sources': [array of strings] }
    """
    #Configure query params
    params = { 'part': 'snippet', 'key': key, 'maxResults': 10 }
    params['playlistId'] = 'PLLQmKWavSS8HJysQrJHkCeW1IZNX55mv3'

    if(page):
        params['pageToken'] = page

    # Make request
    response = requests.get(url=url, params=params).json()

    # Set previous and next page token
    prev_page = ""
    next_page = ""
    if(response.get("prevPageToken")):
        prev_page = response['prevPageToken']
    
    if(response.get('nextPageToken')):
        next_page = response['nextPageToken']

    # Create return dict
    out = { 'nextPageToken': next_page , 'prevPageToken': prev_page, 'totalResults': 0 }
    
    video_list = []

    if(response.get('items')):
        items = response['items']

        # Shuffle contents 
        rnd_gen.shuffle(items)
        
        for item in items:
            id_video = item['snippet']['resourceId']['videoId']
            url_video = source_url + "?v=" + id_video
            video_list.append(url_video)
        
        #Split to contain only result_count items
        video_list = video_list[0:result_count]
        # Add more key-values to out
        out['sources'] = video_list
        out['totalResults'] = len(video_list)
    
    return out



