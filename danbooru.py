import requester, json

file_types = ['jpg', 'jpeg', 'png', 'gif']
url_posts = 'https://danbooru.donmai.us/posts.json'
url_post_view = 'https://danbooru.donmai.us/posts/'
url_root = 'https://danbooru.donmai.us'

def get_image(random=False, page=0):
    params = { 'limit': '5', 'tags': 'takagaki_kaede', 'page': str(page) }

    if(random):
        params['random'] = 'true'

    valid = False
    while(not valid):
        list_images_raw = requester.get_list_images(params=params, url=url_posts)
        list_images = list_images_raw.json()
        num_images = len(list_images)
        print(num_images)
        i = 0

        while(i < num_images and not valid):
            picked_image = list_images[i]
            # Select only with valid tag_string_character
            if(picked_image.get('file_ext') in file_types and 'takagaki_kaede' == picked_image.get("tag_string_character")):
                valid = True
            i += 1
        
    url = url_root + picked_image.get("large_file_url")
    caption = 'Source: ' + url_post_view + str(picked_image.get('id')) + '\n ' + picked_image.get('source')

    #Handle exception if cannot update image TODO

    return {'url': url, 'caption': caption}

def get_image_batch(random=False, page=0, result_count=5):
    params = { 'limit': '5', 'tags': 'takagaki_kaede', 'page': str(page) }
    
    page_random = 25
    picked_images = []

    if(random):
        params['random'] = 'true'

    valid = False
    while(not valid):
        list_images_raw = requester.get_list_images(params=params, url=url_posts)
        list_images = list_images_raw.json()
        num_images = len(list_images)
        print(num_images)
        i = 0

        num_picked = 0
        while(i < num_images and num_picked < result_count-len(picked_images)):
            picked_image = list_images[i]
            # Select only with valid tag_string_character
            if(picked_image.get('file_ext') in file_types and 'takagaki_kaede' == picked_image.get("tag_string_character")):
                num_picked += 1
                picked_images += [list_images[i]]
            i += 1

        if(picked_images and len(picked_images) >= result_count):
            print('valido ' + str(len(picked_images)))
            valid = True
        elif(picked_images and len(picked_images) < result_count):
            print('invalido ' + str(len(picked_images)))
            valid = False
            params['page'] = int(params['page']) + 1

    #Filter information
    result = []

    for image in picked_images:
        url = url_root + image.get("large_file_url")
        caption = 'Source: ' + url_post_view +  str(image.get('id')) + '\n ' + image.get('source')

        result += [{'url': url, 'caption': caption}]

    return result