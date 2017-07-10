import os, requests, json, shutil, copy, danbooru, yandere, konachan

file_types = ['jpg', 'jpeg', 'png', 'gif']
imgboards = ['danbooru', 'konachan', 'yandere']
boards = {'danbooru': 'https://danbooru.donmai.us/posts.json', 'konachan': 'https://konachan.com/post.json', 'yandere': 'https://yande.re/post.json'}

def make_request(url, headers={}, params=None, **kwargs):
	""" requests http/https call for danbooru """
	res = requests.get(url, params=params, headers=headers)
	#print(res.url)
	return res

def get_list_images(params=None, url=None, **kwargs):
	if(url is None):
		url = "https://danbooru.donmai.us/posts.json"
	res = make_request(url, params=params, **kwargs)
	return res

def download_img(url, filename=None, filepath=None):
	if(filename):
		name = filename
	else:
		name = os.path.basename(url)

	if(filepath):
		path = os.path.join(filepath, name)
	else:
		path = os.path.join('images', name)

	# Make request
	res = requests.get(url, stream=True)
	
	# Save image
	with open(path, 'wb') as out:
		shutil.copyfileobj(res.raw, out)
	del res

def get_image(imageboard='danbooru', random=False, page=0):
    """
    imageboard imageboard to download, default is danbooru
    random return random result, default is False
    return a dictionary with url and caption
    """
    if(imageboard == 'danbooru'):
        result = danbooru.get_image(random=random,page=page)
    elif (imageboard == 'konachan'):
        result = konachan.get_image(random=random,page=page)
    elif(imageboard == 'yandere'):
        result = yandere.get_image(random=random,page=page)
    else:
        result = danbooru.get_image(random=random,page=page)

    return result

def get_image_batch(imageboard='danbooru', random=False, page=0, result_count=5):
    """
    TODO enviar foto en cuanto sea valido
    handlear excepciones
    """
    if(imageboard == 'danbooru'):
        result = danbooru.get_image_batch(random=random,page=page,result_count=result_count)
    elif (imageboard == 'konachan'):
        result = konachan.get_image_batch(random=random,page=page,result_count=result_count)
    elif(imageboard == 'yandere'):
        result = yandere.get_image_batch(random=random,page=page,result_count=result_count)
    else:
        result = danbooru.get_image_batch(random=random,page=page,result_count=result_count)

    return result
