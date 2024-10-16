from typing import List


def match(pattern: List[str], source: List[str]) -> List[str]:
    """Attempt to match pattern to source

    % matches a sequence of zero or more words and _ matches any single word

    Args:
        pattern - a pattern using to % and/or _ to extract words from the source
        source - a phrase represented as a list of words (strings)

    Returns:
        None if the pattern and source do not "match" ELSE A list of matched words
        (words in the source corresponding to _'s or %'s, in the pattern, if any)
    """
    sind = 0  # current index we are looking at in the source list
    pind = 0  # current index we are looking at in the pattern list
    result: List[str] = []  # to store the substitutions that we will return if matched

    # keep checking as long as we haven't hit the end of both pattern and source while
    # pind is still a valid index OR sind is still a valid index (valid index means that
    # the index is != to the length of the list)
    while pind != len(pattern) or sind != len(source):
        # 1) check to see if we are at the end of the pattern (from the while condition
        # we know since we already checked to see if you were at the end of the pattern
        # and the source, then you know that if this is True, then the pattern has
        # ended, but the source has not) if we reached the end of the pattern but not
        # source then no match
        if pind == len(pattern):
            return None

        # 2) check to see if the current thing in the pattern is a %
        elif pattern[pind] == "%":
            # at end of pattern grab the rest of the source
            if pind == (len(pattern) - 1):
                return result + [" ".join(source[sind:])]
            else:
                accum = ""
                pind += 1
                while pattern[pind] != source[sind]:
                    accum += " " + source[sind]
                    sind += 1

                    # abort in case we've run out of source with more pattern left
                    if sind >= len(source):
                        return None

                result.append(accum.strip())

        # 3) if we reached the end of the source but not pattern then no match
        elif sind == len(source):
            return None

        # 4) check to see if the current thing in the pattern is an _
        elif pattern[pind] == "_":
            # neither has ended: add a singleton
            result += [source[sind].strip()]
            pind += 1
            sind += 1

        # 5) check to see if the current thing in the pattern is the same as the current
        # thing in the source
        elif pattern[pind] == source[sind]:
            # neither has ended and the words match, continue checking
            pind += 1
            sind += 1

        # 6) this will happen if none of the other conditions are met
        else:
            # neither has ended and the words do not match, no match
            return None

    return result


def get_title(movie: Tuple[str, str, int, List[str]]) -> str:
    return movie[0]


def get_author(movie: Tuple[str, str, int, List[str]]) -> str:
    return movie[1]


def get_year(movie: Tuple[str, str, int, List[str]]) -> int:
    return movie[2]


def get_actors(movie: Tuple[str, str, int, List[str]]) -> List[str]:
    return movie[3]


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


def director_by_title(matches: List[str]) -> List[str]:
    """Finds director of movie based on title

    Args:
        matches - a list of 1 string, just the title

    Returns:
        a list of 1 string, the director of the movie
    """
    title = matches[0]
    result = []
    for movie in movie_db:
        if title == get_title(movie):
            result.append(get_director(movie))
    return result


def title_by_director(matches: List[str]) -> List[str]:
    """Finds movies directed by the passed in director

    Args:
        matches - a list of 1 string, just the director

    Returns:
        a list of movies titles directed by the passed in director
    """
    director = matches[0]
    result = []
    for movie in movie_db:
        if director == get_director(movie):
            result.append(get_title(movie))
    return result


def actors_by_title(matches: List[str]) -> List[str]:
    """Finds actors who acted in the passed in movie title

    Args:
        matches - a list of 1 string, just the movie title

    Returns:
        a list of actors who acted in the passed in title
    """
    title = matches[0]
    result = []
    for movie in movie_db:
        if title == get_title(movie):
            actors = get_actors(movie)
            for actor in actors:
                result.append(actor)
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


def title_by_actor(matches: List[str]) -> List[str]:
    """Finds titles of all movies that the given actor was in

    Args:
        matches - a list of 1 string, just the actor

    Returns:
        a list of movie titles that the actor acted in
    """
    actor = matches[0]
    result = []
    for movie in movie_db:
        if actor in get_actors(movie):
            result.append(get_title(movie))
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