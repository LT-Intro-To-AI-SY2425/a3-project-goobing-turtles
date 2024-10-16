def get_title(movie: Tuple[str, str, int, List[str]]) -> str:
    return movie[0]


def get_author(movie: Tuple[str, str, int, List[str]]) -> str:
    return movie[1]

def get_genre(movie: Tuple[str, str, int, List[str]]) -> str:
    return movie[1]


def get_year(movie: Tuple[str, str, int, List[str]]) -> int:
    return movie[2]



# Below are a set of actions. Each takes a list argument and returns a list of answers
# according to the action and the argument. It is important that each function returns a
# list of the answer(s) and not just the answer itself.


def title_by_year(matches: List[str]) -> List[str]:
    """Finds all movies made in the passed in year

    Args:
        matches - a list of 1 string, just the year. Note that this year is passed as a
            string and should be converted to an int

    Returns:
        a list of movie titles made in the passed in year
    """
    year = int(matches[0])
    result = []
    for movie in movie_db:
        # print(get_year(movie))
        if get_year(movie) == year:
            result.append(get_title(movie))

    return result


def title_by_year_range(matches: List[str]) -> List[str]:
    """Finds all movies made in the passed in year range

    Args:
        matches - a list of 2 strings, the year beginning the range and the year ending
            the range. For example, to get movies from 1991-1994 matches would look like
            this - ["1991", "1994"] Note that these years are passed as strings and
            should be converted to ints.

    Returns:
        a list of movie titles made during those years, inclusive (meaning if you pass
        in ["1991", "1994"] you will get movies made in 1991, 1992, 1993 & 1994)
    """
    start_year = int(matches[0])
    end_year = int(matches[1])
    result = []
    for movie in movie_db:
        if start_year <= get_year(movie) <= end_year:
            result.append(get_title(movie))
    return result


def title_before_year(matches: List[str]) -> List[str]:
    """Finds all movies made before the passed in year

    Args:
        matches - a list of 1 string, just the year. Note that this year is passed as a
            string and should be converted to an int

    Returns:
        a list of movie titles made before the passed in year, exclusive (meaning if you
        pass in 1992 you won't get any movies made that year, only before)
    """
    before_year  = int(matches[0]) 
    result = []
    for movie in movie_db:
        if before_year > get_year(movie):
            result.append(get_title(movie))
    return result 


def title_after_year(matches: List[str]) -> List[str]:
    """Finds all movies made after the passed in year

    Args:
        matches - a list of 1 string, just the year. Note that this year is passed as a
            string and should be converted to an int

    Returns:
        a list of movie titles made after the passed in year, exclusive (meaning if you
        pass in 1992 you won't get any movies made that year, only after)
    """
    after_year = int(matches[0])
    result = []
    for movie in movie_db:
        if after_year < get_year(movie):
            result.append(get_title(movie))
    return result


def author_by_title(matches: List[str]) -> List[str]:
    """Finds author of movie based on title

    Args:
        matches - a list of 1 string, just the title

    Returns:
        a list of 1 string, the author of the movie
    """
    title = matches[0]
    result = []
    for movie in movie_db:
        if title == get_title(movie):
            result.append(get_author(movie))
    return result


def title_by_author(matches: List[str]) -> List[str]:
    """Finds movies directed by the passed in author

    Args:
        matches - a list of 1 string, just the author

    Returns:
        a list of movies titles directed by the passed in author
    """
    director = matches[0]
    result = []
    for movie in movie_db:
        if director == get_author(movie):
            result.append(get_title(movie))
    return result



def year_by_title(matches: List[str]) -> List[int]:
    """Finds year of passed in movie title

    Args:
        matches - a list of 1 string, just the movie title

    Returns:
        a list of one item (an int), the year that the movie was made
    """
    title = matches[0]
    result = []
    for movie in movie_db:
        if title == get_title(movie):
            result.append(get_year(movie))
    return result



# dummy argument is ignored and doesn't matter
def bye_action(dummy: List[str]) -> None:
    raise KeyboardInterrupt


# The pattern-action list for the natural language query system A list of tuples of
# pattern and action It must be declared here, after all of the function definitions
pa_list: List[Tuple[List[str], Callable[[List[str]], List[Any]]]] = [
    (str.split("what movies were made in _"), title_by_year),
    (str.split("what movies were made between _ and _"), title_by_year_range),
    (str.split("what movies were made before _"), title_before_year),
    (str.split("what movies were made after _"), title_after_year),
    # note there are two valid patterns here two different ways to ask for the director
    # of a movie
    (str.split("who directed %"), director_by_title),
    (str.split("who was the director of %"), director_by_title),
    (str.split("what movies were directed by %"), title_by_director),
    (str.split("who acted in %"), actors_by_title),
    (str.split("when was % made"), year_by_title),
    (str.split("in what movies did % appear"), title_by_actor),
    (["bye"], bye_action),
]


def search_pa_list(src: List[str]) -> List[str]:
    """Takes source, finds matching pattern and calls corresponding action. If it finds
    a match but has no answers it returns ["No answers"]. If it finds no match it
    returns ["I don't understand"].

    Args:
        source - a phrase represented as a list of words (strings)

    Returns:
        a list of answers. Will be ["I don't understand"] if it finds no matches and
        ["No answers"] if it finds a match but no answers
    """
    for pat, act in pa_list:
        val = match(pat, src)
        if val != None:
            result = act(val)

            if result == []:
                return ["No answers"]

            return result
        
    result = ["I don't understand"]
    return result 