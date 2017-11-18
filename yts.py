import requests
from bs4 import BeautifulSoup
import csv

for i in range(1,400):
    index = "https://yts.ag/browse-movies?page=2"
    index = index.replace('2',str(i))
    page = requests.get(index)
    soup = BeautifulSoup(page.content, 'html.parser')
    for movie in soup.find_all('a', class_="browse-movie-link"):
        movie_index = movie.get('href')
        movie_page = requests.get(movie_index)
        movie_soup = BeautifulSoup(movie_page.content, 'html.parser')
        for film_content in movie_soup.find_all('div', id="movie-content"):
            film = film_content.find('div', id="movie-info")
            movie_title_box = film.find('h1')
            #movie_title
            movie_title = movie_title_box.text
            print(i, movie_title)
            movie_year_box = film.find('h2')
            #movie_year
            movie_year = movie_year_box.text
            movie_genre_box = film.select("h2:nth-of-type(2)")
            #movie_genre
            movie_genre = movie_genre_box[0].text
            movie_likes_box = film.find('span', {"id":"movie-likes"})
            #movie_likes
            movie_likes = movie_likes_box.text
            movie_imdb_box = film.find('span',{"itemprop":"ratingValue"})
            #movie_imdb
            movie_imdb = movie_imdb_box.text
            film_spec = film_content.find('div', attrs={"id":"movie-tech-specs"})
            movie_cert_box = film_spec.select("div:nth-of-type(9)")
            #movie_cert
            try:
                movie_cert = movie_cert_box[0].text
            except IndexError:
                movie_cert = "NA"
            movie_time_box = film_spec.select("div:nth-of-type(16)")
            #movie_time
            try:
                movie_time = movie_time_box[0].text
            except IndexError:
                movie_time = "NA"
            #write movie details to file
            with open('yts.csv', 'a') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow([movie_title, movie_year, movie_genre, movie_likes, movie_imdb, movie_cert, movie_time, movie_index])

            
