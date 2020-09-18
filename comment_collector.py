from typing import List, Set
from psaw import PushshiftAPI
import gzip


def store_compressed_data(data: List[str], outfile_path: str):
    """Write gzip compressed data out to file newline-separated

    Args:
        data (List[str]): List of strings to write out to file
        outfile_path (str): File path to write to
    """
    with gzip.open(outfile_path, "wb") as outfile:
        for datum in data:
            outfile.write(bytearray(datum, "utf8"))
            outfile.write(b"\n")


def read_compressed_data(infile_path: str) -> List[str]:
    """Read data stored in gzip compressed file

    Args:
        infile_path (str): Path to gzip compressed file

    Returns:
        List[str]: List of lines from file
    """
    with gzip.open("test.gz", "rb") as file:
        file_content = file.read().decode()
    return file_content.split("\n")[:-1]


def get_user_comments(username: str, api: PushshiftAPI) -> List[str]:
    """Get all of a user's comment history

    Args:
        username (str): Reddit username to scrape comments
        api (PushshiftAPI): Instance of Pushshift API

    Returns:
        List[str]: Text contents of all comments
    """
    comments = []
    comment_generator = api.search_comments(author=username, filter=["body"], limit=500)
    for comment in comment_generator:
        comments.append(comment.body)
    return comments


def get_usernames_from_file(infile_path: str) -> List[str]:
    """Get all usernames from newline separated file

    Args:
        infile_path (str): Path to newline separated file of usernames

    Returns:
        List[str]: Usernames in file
    """
    with open(infile_path, "r") as file:
        usernames = file.read()
    return usernames.split("\n")[:-1]


def store_comments_for_users(
    usernames: List[str], api: PushshiftAPI, outfile_prefix="data"
):
    """Store comments in gzipped file for users

    Args:
        usernames (List[str]): List of users to scrape comments for
        api (PushshiftAPI): Pushshift API instance
        outfile_prefix (str, optional): Prefix for outfile path. Defaults to "data".
    """
    for user in usernames:
        comments = get_user_comments(user, api)
        store_compressed_data(comments, f"{outfile_prefix}/{user}.gz")