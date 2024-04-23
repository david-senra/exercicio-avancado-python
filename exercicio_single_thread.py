import requests
import time
import csv
import random

from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/39.0.2171.95 Safari/537.36',
           'Accept-Language': 'pt-BR'}  # headers usados na request


def extract_movie_details(movie_link):
    time.sleep(random.uniform(0, 0.2))
    response = BeautifulSoup(requests.get(movie_link, headers=headers).content, 'html.parser')

    if response is not None:

        movie_position = response.find('div', class_='sc-5f7fb5b4-1 fTREEx')
        movie_data_1 = response.find('div', class_='sc-b7c53eda-0 dUpRPQ')
        movie_score = response.find('div', class_='sc-bde20123-2 cdQqzc')
        movie_plot = response.find('p', class_='sc-466bb6c-3 fOUpWp')

        if movie_position is None:
            ranking = 'ND'
        else:
            ranking = movie_position.get_text()

        if movie_plot is None:
            plot = 'ND'
        else:
            plots = movie_plot.find_all('span')
            plot_full = plots[2]
            plot = plot_full.get_text()

        if movie_score is None:
            audience_score = 'ND'
        else:
            audience_score = movie_score.find('span').get_text()

        if movie_data_1 is None:
            title = 'ND'
            date = 'ND'
            parental_rating = 'ND'
            duration = 'ND'
        else:
            title = movie_data_1.find('span', class_='hero__primary-text').get_text()
            other_data = movie_data_1.find_all('li')
            date = other_data[0].find('a').get_text()
            if len(other_data) > 2:
                parental_rating = other_data[1].find('a').get_text()
                duration = other_data[2].get_text()
            elif len(other_data) < 2:
                parental_rating = 'ND'
                duration = 'ND'
            else:
                if other_data[1].find('a') is None:
                    duration = other_data[1].get_text()
                    parental_rating = 'ND'
                else:
                    duration = "ND"
                    parental_rating = other_data[1].find('a').get_text()

        with open('filmes_single_thread.csv', mode='a') as f:
            movie_writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            if all([title]):
                print(ranking, title, date, duration, parental_rating, audience_score, plot)
                movie_writer.writerow([ranking, title, date, duration, parental_rating, audience_score, plot])


def extract_movies(soup):
    all_movies = soup.find('ul', class_='ipc-metadata-list ipc-metadata-list--dividers-between sc-a1e81754-0 eBRbsI '
                                        'compact-list-view ipc-metadata-list--base')
    movies_list = all_movies.find_all('li')
    movie_links = ["https://imdb.com" + movie.find("a")["href"] for movie in movies_list]

    for movie_link in movie_links:
        extract_movie_details(movie_link)


def main():
    start_time = time.time()

    # IMDB Mais Populares - 100 filmes
    popular_movies_url = 'https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm'
    response = requests.get(popular_movies_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Função principal - extrai a lista com os 100 filmes
    extract_movies(soup)

    end_time = time.time()
    time_taken = end_time - start_time
    print('Tempo total da operação: ', time_taken)
    with open('filmes_single_thread.csv', mode='a') as f:
        movie_writer = csv.writer(f, delimiter=':', quoting=csv.QUOTE_MINIMAL)
        movie_writer.writerow(["Tempo decorrido", time_taken])


if __name__ == '__main__':
    main()
