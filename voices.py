import random, os

voice_path = 'voices'
types = {'introduction': 'introduction', 'home': 'home', 'affection': 'affection', 'live':'live', 'room': 'room' }

def get_voice(type_voice='random'):
    """
    Returns the path of a specific voice type clip or a random one 
    """
    if(type_voice == 'random'):
        list_types = list(types.keys())
        type_voice = list_types[random.randrange(len(list_types))]
    elif (not type_voice in list(types.keys())):
        raise RuntimeError("Valid voice types: {0}".format(list(types.keys())))

    filepath = os.path.join(voice_path, types.get(type_voice))
    list_files = os.listdir(filepath)
    filename = list_files[random.randrange(len(list_files))]
    filepath = os.path.join(filepath,filename)

    return filepath