import requests
from bs4 import BeautifulSoup

class Scraper:

    def __init__(self):
        self.__title_selection_class = "lister-item-header"
        self.__rating_selection_class = "inline-block ratings-imdb-rating"
        self.__genre_selection_class = "genre"
        self.__year_selection_class = "lister-item-year text-muted unbold"

    
    def __get_page(self, url) -> list:
        headers = {'Accept-Language': 'en-US,en;q=0.5'}
        response = requests.get(url, headers=headers)

        print(response.status_code)

        
        if response.status_code != 200:
            raise Exception(f'Failed to load page {url}')
        
        doc = BeautifulSoup(response.text, 'html.parser')
        return doc


    def __get_movie_titles(self, doc) -> list:
        movie_title_tags = doc.find_all('h3', {'class': self.__title_selection_class})
        movie_titles = []

        for tag in movie_title_tags:
            title = tag.find('a').text
            movie_titles.append(title)

        return movie_titles


    def __get_movie_rating(self, doc) -> list:
        movie_rating_tags = doc.find_all('div', {'class': self.__rating_selection_class})
        movie_ratings = []

        for tag in movie_rating_tags:
            rating = tag.get_text().strip()
            movie_ratings.append(rating)

        return movie_ratings


    def __get_movie_genre(self, doc) -> list:
        movie_genre_tags=doc.find_all('span',{'class': self.__genre_selection_class})
        movie_genre=[]

        for tag in movie_genre_tags:
            genre = tag.get_text().strip()
            genre = genre.split(", ")
            movie_genre.append(genre)

        return movie_genre


    def __get_movie_year(self, doc) -> list:
        movie_year_tags=doc.find_all('span',{'class': self.__year_selection_class})
        released_year=[]

        for tag in movie_year_tags:
            year = tag.get_text().strip()[1:5]
            released_year.append(year)

        return released_year


    def __get_director(self, doc) -> list:
        director_tags=doc.find_all('p', class_ = '')
        directors=[]

        for tag in director_tags:
            if tag.find_next().name == 'a':
                directors.append(tag.find_next().text)
            
        return directors


    def get_top250_movies_info(self):
        movies_dict = {
            'titles': [],
            'genre': [],
            'rating': [],
            'year': [],
            'director': []
        }

        for i in range(1, 250, 50):
            url = f"https://www.imdb.com/search/title/?groups=top_250&start{str(i)}&ref_=adv_next"
            doc = self.__get_page(url)

            movies_dict['titles'] += self.__get_movie_titles(doc)
            movies_dict['rating'] += self.__get_movie_rating(doc)
            movies_dict['year'] += self.__get_movie_year(doc)
            movies_dict['genre'] += self.__get_movie_genre(doc)
            movies_dict['director'] += self.__get_director(doc)  
            
        return movies_dict


    def get_movies_by_genres(self, genres):
        movies_dict = {
            'titles': [],
            'rating': [],
            'year': [],
            'genre': [],
            'director': []
        }

        for i in range(1, 250, 50):
            url = f"https://www.imdb.com/search/title/?genres={genres}&start={str(i)}&explore=title_type,genres"
            doc = self.__get_page(url)

            movies_dict['titles'] += self.__get_movie_titles(doc)
            movies_dict['rating'] += self.__get_movie_rating(doc)
            movies_dict['year'] += self.__get_movie_year(doc)
            movies_dict['genre'] += self.__get_movie_genre(doc)
            movies_dict['director'] += self.__get_director(doc)  

        return movies_dict


    ### 403 unauthorized ###
    #TODO! need to use selenium i guess
    def get_celeb_info(self, name):
        search_url = f"https://www.imdb.com/find/?s=nm&q=dana&ref_=nv_sr_sm"
#        search_url = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"
        doc = self.__get_page(search_url)
        print(doc)


test = Scraper()
test.get_celeb_info('zack snyder')
