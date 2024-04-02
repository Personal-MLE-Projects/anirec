import requests
from bs4 import BeautifulSoup


def get_users():

    url = f'https://myanimelist.net/users.php'

    users = []

    for i in range(250):

        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

        else:
            print("Failed to retrieve the webpage.")

        users_raw = str(soup).split('<tr>')[2].split('/profile/')

        for i in users_raw:

            user_i = i.split('"')[0]
            if user_i != '<td align=':
                users.append(user_i)
            else:
                pass

    users = list(set(users))

    with open('./../outputs/users.txt', 'w') as fp:
        for user in users:
            # write each item on a new line
            fp.write("%s\n" % user)
        print('Done')


    return users


  

if __name__ == '__main__':
    
    get_users()