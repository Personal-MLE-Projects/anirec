from bs4 import BeautifulSoup
import requests
import pandas as pd

def scrape_user_info(users):

  total_ratings = {}

  for user in users:

    url = f'https://myanimelist.net/animelist/{user}?status=2'

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        article_titles = soup.find_all('tbody', class_='article-title')
        for title in article_titles:
            print(title.text.strip())
    else:
        print("Failed to retrieve the webpage.")
    try:
      scraped_list = str(soup).split('data-items')[1].split('&quot;')
      names = []
      scores = []

      for i in range(len(scraped_list) - 1):
        if scraped_list[i] == 'anime_title':
          names.append(scraped_list[i + 2])

        if scraped_list[i] == 'score':
          scores.append(scraped_list[i + 1])


      scores_new = [int(s[1:2]) for s in scores]

      user_ratings = {}

      for n,s in zip(names,scores_new):
        user_ratings[n] = s

      total_ratings[user] = user_ratings
      print(f'{user.upper()} SCRAPED!')
    except:
      print('Could not be scraped.')


  return total_ratings


def get_csv(users):
    ratings = pd.DataFrame(columns=['user','title','rating'])

    for key,value in users.items():
        if len(value) > 0:
            df = pd.DataFrame(list(value.items()), 
                            columns=['title', 'rating'])
            df['user'] = [key]*len(value)
            ratings = pd.concat([ratings,df],axis=0)

    return ratings


if __name__ == '__main__':
    read_path = "./outputs/users.txt"

    with open(read_path, "r") as file:
        users = file.readlines()
        users = [line.strip() for line in users]

    ratings_hm = scrape_user_info(users[:10])

    ratings = get_csv(ratings_hm)

    output_path = './outputs/ratings.csv'

    ratings.to_csv(output_path,index=False)

    

