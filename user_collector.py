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


def confirm_user_dislikes_coffee(comment_body: str) -> bool:
    """Confirm that the user who wrote the given comment dislikes coffee

    Args:
        comment_body (str): Body of comment that may express dislike of coffee

    Returns:
        bool: True if the user dislikes coffee
    """
    print(comment_body)
    user_confirmation = input(
        "\n Does the above comment indicate dislike? (y/n): "
    ).lower()
    if user_confirmation not in {"y", "n"}:
        print("Please enter either 'y' or 'n'")
        return confirm_user_dislikes_coffee(comment_body)
    return user_confirmation == "y"


def find_coffee_dislikers(num_users: int, api: PushshiftAPI) -> List[str]:
    """Find users who dislike coffee in an interactive manner

    Args:
        num_users (int): Number of users to find
        api (PushshiftAPI): Instance of PushshiftAPI

    Returns:
        List[str]: List of users that do not like coffee
    """
    usernames: Set[str] = set()
    comment_gen = api.search_comments(
        q='"I don\'t like coffee"', filter=["author", "body"]
    )
    for comment in comment_gen:
        if comment.author == "[deleted]":
            continue
        users_remaining = num_users - len(usernames)
        if users_remaining == 0:
            break
        print(f"\nUsers remaining: {users_remaining}\n")
        if comment.author in usernames or len(comment.body) > 200:
            continue
        if confirm_user_dislikes_coffee(comment.body):
            usernames.add(comment.author)
    return list(usernames)
