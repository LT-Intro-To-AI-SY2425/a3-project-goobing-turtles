#  Include the book database, named book_db
from books import book_db
from match import match
from typing import List, Tuple, Callable, Any


def get_title(book: Tuple[str, str, str, int]) -> str:
    return book[0]


def get_author(book: Tuple[str, str, str, int]) -> str:
    return book[1]

def get_genre(book: Tuple[str, str, str, int]) -> str:
    return book[2]


def get_year(book: Tuple[str, str, str, int]) -> int:
    return book[3]



# Below are a set of actions. Each takes a list argument and returns a list of answers
# according to the action and the argument. It is important that each function returns a
# list of the answer(s) and not just the answer itself.


def title_by_year(matches: List[str]) -> List[str]:
    """Finds all books made in the passed in year

    Args:
        matches - a list of 1 string, just the year. Note that this year is passed as a
            string and should be converted to an int

    Returns:
        a list of book titles made in the passed in year
    """
    year = int(matches[0])
    result = []
    for book in book_db:
        # print(get_year(book))
        if get_year(book) == year:
            result.append(get_title(book))

    return result

def genre_by_year(matches: List[str]) -> List[str]:
    """Finds all books made in the passed in year

    Args:
        matches - a list of 1 string, just the year. Note that this year is passed as a
            string and should be converted to an int

    Returns:
        a list of book titles made in the passed in year
    """
    genre = int(matches[0])
    result = []
    for book in book_db:
        if get_genre(book) == genre:
            result.append(get_genre(book))

    return result


def title_by_year_range(matches: List[str]) -> List[str]:
    """Finds all books made in the passed in year range

    Args:
        matches - a list of 2 strings, the year beginning the range and the year ending
            the range. For example, to get books from 1991-1994 matches would look like
            this - ["1991", "1994"] Note that these years are passed as strings and
            should be converted to ints.

    Returns:
        a list of book titles made during those years, inclusive (meaning if you pass
        in ["1991", "1994"] you will get books made in 1991, 1992, 1993 & 1994)
    """
    start_year = int(matches[0])
    end_year = int(matches[1])
    result = []
    for book in book_db:
        if start_year <= get_year(book) <= end_year:
            result.append(get_title(book))
    return result


def title_before_year(matches: List[str]) -> List[str]:
    """Finds all books made before the passed in year

    Args:
        matches - a list of 1 string, just the year. Note that this year is passed as a
            string and should be converted to an int

    Returns:
        a list of book titles made before the passed in year, exclusive (meaning if you
        pass in 1992 you won't get any books made that year, only before)
    """
    before_year  = int(matches[0]) 
    result = []
    for book in book_db:
        if before_year > get_year(book):
            result.append(get_title(book))
    return result 


def title_after_year(matches: List[str]) -> List[str]:
    """Finds all books made after the passed in year

    Args:
        matches - a list of 1 string, just the year. Note that this year is passed as a
            string and should be converted to an int

    Returns:
        a list of book titles made after the passed in year, exclusive (meaning if you
        pass in 1992 you won't get any books made that year, only after)
    """
    after_year = int(matches[0])
    result = []
    for book in book_db:
        if after_year < get_year(book):
            result.append(get_title(book))
    return result


def author_by_title(matches: List[str]) -> List[str]:
    """Finds author of book based on title

    Args:
        matches - a list of 1 string, just the title

    Returns:
        a list of 1 string, the author of the book
    """
    title = matches[0]
    result = []
    for book in book_db:
        if title == get_title(book):
            result.append(get_author(book))
    return result


def title_by_author(matches: List[str]) -> List[str]:
    """Finds books directed by the passed in author

    Args:
        matches - a list of 1 string, just the author

    Returns:
        a list of books titles directed by the passed in author
    """
    author = matches[0]
    result = []
    for book in book_db:
        if author == get_author(book):
            result.append(get_title(book))
    return result



def year_by_title(matches: List[str]) -> List[int]:
    """Finds year of passed in book title

    Args:
        matches - a list of 1 string, just the book title

    Returns:
        a list of one item (an int), the year that the book was made
    """
    title = matches[0]
    result = []
    for book in book_db:
        if title == get_title(book):
            result.append(get_year(book))
    return result



# dummy argument is ignored and doesn't matter
def bye_action(dummy: List[str]) -> None:
    raise KeyboardInterrupt


# The pattern-action list for the natural language query system A list of tuples of
# pattern and action It must be declared here, after all of the function definitions
pa_list: List[Tuple[List[str], Callable[[List[str]], List[Any]]]] = [
    (str.split("what books were written in _"), title_by_year),
    (str.split("what books were written between _ and _"), title_by_year_range),
    (str.split("what books were written before _"), title_before_year),
    (str.split("what books were written after _"), title_after_year),
    # note there are two valid patterns here two different ways to ask for the author
    # of a book
    (str.split("who wrote %"), author_by_title),
    (str.split("who was the author of %"), author_by_title),
    (str.split("what books were written by %"), title_by_author),
    (str.split("when was % released"), year_by_title),
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