import requests, random, json

client_id = ''
album_hash = ''
url = 'https://api.imgur.com/3/album/'

def get_random_card(count=1):
    """
    Makes a api requests to Imgur getting a number of images from the card album and returns a list of image links
    """
    url_request = url + album_hash + '/images'
    headers = {'Authorization': 'Client-ID ' + client_id}
    res = requests.get(url_request, headers=headers)
    res_json = res.json()
    
    if(res_json.get('status') != 200):
        # Throws a rutime error if the request wasnt succesfull
        raise RuntimeError(str(res_json.get('status')))
    else:
        image_list = res_json.get('data')
        picked_images = []
        dump_images = []
        size = len(image_list)
        for i in range(0, count):
            image = image_list.pop(random.randrange(size))
            picked_images.append(image.get('link'))
            #Update size variable because we deleted one image from the list
            size = len(image_list)
            # Add picked image to the dump image list
            dump_images.append(image)
            # If the size of the image_list is zero, swap it with dump_images list
            if(size == 0):
                image_list = dump_images
                dump_images = []
                size = len(image_list)
        
        return picked_images