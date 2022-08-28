import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

def get_movie(list_url):
    """
    Given a shuffled list url from letterboxd, it will return a tuple containing the film title, rating, and
    url for poster

    :param url: A string representing the url of a list on letterboxd
    :return: A tuple of the first film in the input film containing (film title, rating)
        film title - A string representing the title of the film and its release year
        rating - A float of the film rating
    """
    list_page = requests.get(list_url)
    # Use soup to make it readable
    list_page_soup = BeautifulSoup(list_page.content, "html.parser")
    # Find the first movie in the list
    classthing = list_page_soup.find("li", class_= "poster-container numbered-list-item")

    classthingstring = str(classthing)
    # print(string)
    # Look for the idx of the link so we can get to a movie
    idx = classthingstring.find("data-film-slug=")
    # only iterate over where the link is located in the string
    slicedstring = classthingstring[idx + 16:]
    # get the /'filmtitle'/ suffix of the link
    suff_link = ""
    c = 0
    for char in slicedstring:
        if char == "/":
            c += 1
        suff_link += char
        if c == 3:
            break

    # now we have the link for the movie we'll get info from
    movielink = "http://letterboxd.com" + suff_link
    moviepage = requests.get(movielink)
    moviesoup = BeautifulSoup(moviepage.content, "html.parser")

    # get the title of the film
    title_line = moviesoup.find("meta", attrs={'property': "og:title"})
    title_str = str(title_line)
    counter = 0
    title = ""
    for char in title_str:
        if char == '"':
            counter += 1
            continue
        if counter == 1:
            title = title + char
        if counter == 2:
            break

    # get the rating for the film
    moviepage = requests.get(movielink)
    moviesoup = BeautifulSoup(moviepage.content, "html.parser")
    rating_line = moviesoup.find("meta", attrs={'name':"twitter:data2"})
    rating_str = str(rating_line)
    rating = float(rating_str[15:19])
    rating = str(rating)

    #get the link of the poster for the image
    poster_url = get_poster(movielink)

    return (title, rating, poster_url)

def get_poster(movie_url):
    """
    Helper function for get_movie which finds the poster url

    :param movie_url: a string that is a link to a film page on letterboxd
    :return: a string that represents a poster
    """
    moviepage = requests.get(movie_url)
    moviesoup = BeautifulSoup(moviepage.content, "html.parser")

    # get the line containing the film id
    id_line = moviesoup.find("body", class_ = "film backdropped")
    id_str = str(id_line)

    # search for the actual tmdb film id
    counter = 0
    id = ""
    for char in id_str:
        if char == '"':
            counter += 1
            if counter > 3:
                break
            continue
        if char.isdigit():
            id = id + char

    # scrape from the tmdb page of the movie we're looking at
    tmdb_movie_link = "https://www.themoviedb.org/movie/" + id
    hdr = {'User-Agent': 'Mozilla/5.0'}
    # FIX THIS URLOPEN DOESN'T WORK???
    tmdb_req = Request(tmdb_movie_link, headers=hdr)
    tmdb_movie_page = urlopen(tmdb_req)
    tmdb_movie_soup = BeautifulSoup(tmdb_movie_page, "html.parser")

    # find the line with the poster url
    poster_url_line = tmdb_movie_soup.find("img", {"class" : "poster"})
    poster_url_str = str(poster_url_line)

    # get the actual poster url
    poster_url = ""
    counter = 0
    for char in poster_url_str:
        if char == '"':
            counter += 1
            if counter > 5:
                break
            continue
        if counter == 5:
            poster_url = poster_url + char
    return "https://image.tmdb.org" + poster_url

print(get_movie("https://letterboxd.com/joeibanez/list/the-100-most-watched-films-on-letterboxd/by/shuffle/"))