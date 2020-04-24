try:
    import vk_api
except ImportError:
    print('Module \'vk_api\' is not installed in this envirovement. Use \'pip3 install vk_api\' for install this.'); exit()

import time
import os

def screen_cleaning():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def clean_profileInfo():
    vk.method('account.saveProfileInfo', {'relation': 0, 'bdate': '1.1.1970', 'bdate_visibility': 0, 'home_town': '', 'country_id': 0, 'city_id': 0, 'status': ''})

def clean_friends():
    while vk.method('friends.get')['count'] != 0:
        for user_id in vk.method('friends.get', {'count': 10000})['items']:
            vk.method('friends.delete', {'user_id': user_id})

    while vk.method('friends.getRequests', {'out': 1})['count'] != 0:
        for user_id in vk.method('friends.getRequests', {'count': 1000, 'out': 1})['items']:
            vk.method('friends.delete', {'user_id': user_id})

def clean_subscribtions():
    subscribers = []
    count_of_dogs = 0

    while vk.method('users.getFollowers')['count'] != count_of_dogs:
        for user_id in vk.method('users.getFollowers', {'count': 1000})['items']:
            try:
                vk.method('account.ban', {'owner_id': user_id})
            except vk_api.exceptions.ApiError: # At this moment can raised only if user blocked or his page deleted
                count_of_dogs += 1
            subscribers.append(user_id)
        time.sleep(1200)
        for user_id in subscribers:
            vk.method('account.unban', {'owner_id': user_id})

    del(subscribers, count_of_dogs)

    while vk.method('users.getSubscriptions')['users']['count'] != 0:
        for user_id in vk.method('users.getSubscriptions', {'count': 200}):
            vk.method('friends.delete', {'user_id': user_id})
            time.sleep(1)

    while vk.method('users.getSubscriptions')['groups']['count'] != 0:
        for group_id in vk.method('users.getSubscriptions', {'count': 200}):
            vk.method('groups.leave', {'group_id': group_id})
            time.sleep(1)

def clean_messages():
    while vk.method('messages.getConversations')['count'] != 0:
        for chat in vk.method('messages.getConversations', {'count': 200})['items']:
            vk.method('messages.deleteConversation', {'user_id': chat['conversation']['peer']['id']})
            time.sleep(1)

def clean_groups(): 
    while vk.method('groups.get')['count'] != 0:
        for group_id in vk.method('groups.get', {'count': 1000})['items']:
            vk.method('groups.leave', {'group_id': group_id})
            time.sleep(1)

def clean_photos():
    while vk.method('photos.getAll')['count'] != 0:
        for photo in vk.method('photos.getAll', {'count': 200})['items']:
            vk.method('photos.delete', {'photo_id': photo['id']})
            time.sleep(1)
                                               
    while vk.method('photos.getAlbums')['count'] != 0:
        for album in vk.method('photos.getAlbums')['items']:
            vk.method('photos.deleteAlbum', {'album_id': album['id']})
            time.sleep(1)

def clean_videos():
    while vk.method('video.get')['count'] != 0:
        for video in vk.method('video.get', {'count': 200}):
            vk.method('video.delete', {'video_id': video['id']})
            time.sleep(1)

def clean_wall():
    while vk.method('wall.get')['count'] != 0:
        for post in vk.method('wall.get', {'count': 100})['items']:
            vk.method('wall.delete', {'post_id': post['id']})
            time.sleep(1)

app_id = '2685278' # Kate Mobile Application ID. Required for 'messages.*' bypass

screen_cleaning()

try:
    print('VK Cleaner by Oleg Voevodin')

    auth_mode = input('Login using token or password? (t/p): ')

    if auth_mode.lower() == 'p':
        login = input('VK login: ')
        password = input('VK password: ')
        try:
            vk = vk_api.VkApi(login=login, password=password, app_id=app_id, auth_handler=lambda: [input('2FA code: '), False])
            vk.auth()
            print('Access granted!')
        except vk_api.exceptions.BadPassword:
            print('Incorrect password. Goodbye!'); exit()
        except (vk_api.exceptions.TwoFactorError, vk_api.exceptions.AuthError):
            print('Wrong 2FA code. Goodbye!'); exit()
    elif auth_mode.lower() == 't':
        token = input('VK token: ')
        try:
            vk = vk_api.VkApi(token=token)
            vk.method('status.get') # Method, which using for auth testing
            print('Access granted!')
        except vk_api.exceptions.ApiError: # At this moment can raised only if token is invalid
            print('Invalid token!'); exit()

    print('\nUsing this program, you can erase: \n\t1. Profile Info\n\t2. Friends\n\t3. Subscribtions\n\t4. Messages\n\t5. Groups\n\t6. Photos\n\t7. Videos\n\t8. Wall\n\t[!] 9. Clean EVERYTHING')
    print('\nEnter numbers of things, which you want to erase. Like \'1\', \'4\', \'567\', \'247\'. If you want to erase everything, enter \'9\' only.')

    choice = input('\nYou choice: ')
    
    for number in choice:
        if number == '1':
            clean_profileInfo()
        elif number == '2':
            clean_friends()
        elif number == '3':
            clean_subscribtions()
        elif number == '4':
            clean_messages()
        elif number == '5':
            clean_groups()
        elif number == '6':
            clean_photos()
        elif number == '7':
            clean_videos()
        elif number == '8':
            clean_wall()
        elif number == '9':
            clean_profileInfo()
            clean_friends()
            clean_subscribtions()
            clean_messages()
            clean_groups()
            clean_photos()
            clean_videos()
            clean_wall()
        else:
            print(f'Unknown choice \'{number}\'.')

    print('Good luck!'); exit()
    
except KeyboardInterrupt:
    print('Goodbye! :D')
