import requester, json
import random as rnd_gen

file_types = ['jpg', 'jpeg', 'png', 'gif']
url_posts = 'https://konachan.com/post.json'
url_post_view = 'https://konachan.com/post/show/'

def get_image(random=False, page=0):
    params = { 'limit': '5', 'tags': 'takagaki_kaede', 'page': str(page) }
    page_random = 25

    valid = False
    while(not valid):
        if(random):
            params['page'] = rnd_gen.randrange(page_random) # random between 0 and page_random
        
        list_images_raw = requester.get_list_images(params=params, url=url_posts)
        list_images = list_images_raw.json()
        num_images = len(list_images)
        print(num_images)

        if(list_images and random):
            print('has image')
            picked_image = list_images[rnd_gen.randrange(num_images)]        
            valid = True
        elif (list_images):
            print('has image')
            picked_image = list_images[0]
            valid = True
        else:
            if(page_random > 0):
                page_random -= 5
            else:
                page_random += 5
            valid = False
    
    url = 'https:' + picked_image.get('file_url')
    caption = 'Source: ' + url_post_view + str(picked_image.get('id')) + '\n' + picked_image.get('source')

    #Handle exceptions if cannot update image TODO

    return {'url': url, 'caption': caption}

def get_image_batch(random=False, page=0, result_count=5):
    params = { 'limit': '5', 'tags': 'takagaki_kaede', 'page': str(page) }
    page_random = 25
    picked_images = []

    valid = False
    while(not valid):
        if(random):
            params['page'] = rnd_gen.randrange(page_random) # random between 0 and page_random

        list_images_raw = requester.get_list_images(params=params, url=url_posts)
        list_images = list_images_raw.json()
        num_images = len(list_images)
        print(num_images)

        if(list_images and random):
            print('has image')
            first_index = rnd_gen.randrange(num_images)
            picked_images = picked_images + list_images[first_index:first_index+result_count]        
        elif (list_images):
            print('has image')
            picked_images = picked_images + list_images[0:result_count] # Aqui va mal por latest
        else:
            if(page_random > 0):
                page_random -= 5
            else:
                page_random += 5
            valid = False

        if(picked_images and len(picked_images) >= result_count):
            valid = True
        elif(picked_images and len(picked_images) < result_count):
            valid = False
            params['page'] = int(params['page']) + 1

    # Filter information
    result = []

    for image in picked_images:
        url = 'https:' +  image.get('file_url')
        caption = 'Source: ' + url_post_view + str(image.get('id')) + '\n' + image.get('source')

        result += [{'url': url, 'caption': caption}]
    
    return result
