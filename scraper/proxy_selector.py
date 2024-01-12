"""Random Proxy Selector."""

import random
from typing import Dict, List


def read_proxy_list(path: str) -> List[str]:
    with open(path, "r") as file:
        lines = [line.strip() for line in file]
    return lines


def select_proxy(proxies: list) -> Dict[str, str]:
    proxy = random.choice(proxies)

    return {
        "server": proxy.split("@")[1],
        "username": proxy.split("@")[0].split(":")[0],
        "password": proxy.split("@")[0].split(":")[1],
    }


# # Specify the path to your text file
# file_path = 'your_file.txt'

# # Use list comprehension to read and strip each line
# with open(file_path, 'r') as file:
#     lines = [line.strip() for line in file]

# # Print or use the list of lines
# print(lines)
