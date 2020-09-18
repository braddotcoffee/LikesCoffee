from typing import List, Set
from psaw.PushshiftAPI import PushshiftAPI


def store_raw_data(data: List[str], outfile_path: str):
    """Write raw data out to file newline-separated

    Args:
        data (List[str]): List of strings to write out to file
        outfile_path (str): File path to write to
    """
    with open(outfile_path, "w") as outfile:
        for datum in data:
            outfile.write(datum)
            outfile.write("\n")


def find_coffee_hobbyist_users(num_users: int, api: PushshiftAPI) -> List[str]:
    """Find users who comment in coffee hobbyist subreddits

    Args:
        num_users (int): Number of unique users to find
        api (PushshiftAPI): Instance of Pushshift API

    Returns:
        List[str]: List of Reddit usernames
    """
    usernames: Set[str] = set()
    comment_gen = api.search_comments(subreddit="coffee", filter=["author"])
    for comment in comment_gen:
        if comment.author == "[deleted]":
            continue
        usernames.add(comment.author)
        if len(usernames) == num_users:
            break
    return list(usernames)


if __name__ == "__main__":
    hobbyist_users = find_coffee_hobbyist_users(1000, PushshiftAPI())
    training_users = hobbyist_users[:500]
    testing_users = hobbyist_users[500:900]
    vault_users = hobbyist_users[900:]
    store_raw_data(training_users, "data/training_users.txt")
    store_raw_data(testing_users, "data/testing_users.txt")
    store_raw_data(vault_users, "data/vault_users.txt")
