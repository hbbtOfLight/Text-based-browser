import sys
import shutil
import os
import requests
from bs4 import BeautifulSoup
from colorama import Fore


back_list = list()
prev_path = str()
https_prefix = "https://"


def create_dir(dir: str):
    if not os.access(dir, os.F_OK):
        os.mkdir(dir)


# def check_uri(uri: str):
#     if uri != "bloomberg.com" and uri != "nytimes.com":
#         print("Error message")
#         return False
#     return True

def create_file_name(uri: str):
    parts_tuple = uri.rsplit(".")
    if parts_tuple[0].startswith(https_prefix):
        # print(parts_tuple[0].split(https_prefix))
        return parts_tuple[0].split(https_prefix)[1]
    return parts_tuple[0]


#########################################################
def make_request(uri: str):
    if not uri.startswith(https_prefix):
        uri = https_prefix + uri
    #print(requests.get(uri).text)
    return requests.get(uri)


def process_request(my_request):
    soup = BeautifulSoup(my_request.content, 'html.parser')
    for link in soup.findAll('a'):
        link.string = "".join([Fore.BLUE, link.get_text(), Fore.RESET])

    return soup.get_text()




def process_uri(dir: str, uri: str):
    global prev_path
    my_request = None
    try:
        my_request = make_request(uri)
    except requests.exceptions.ConnectionError:
        print("Incorrect URL")
        return
    back_list.append(prev_path)
    create_dir(dir)
    full_path = os.path.join(dir, create_file_name(uri))
    with open(full_path, "w", encoding="utf-8") as fp:
        fp.write(process_request(my_request))
    print_content(full_path)
    prev_path = full_path


def print_content(full_path):
    with open(full_path, "r", encoding="utf-8") as fp:
        print(fp.read())


def print_back():
    back_path = back_list.pop()
    print_content(back_path)


# write your code here
dir = sys.argv[1]
toexit = False
while not toexit:
    request_ = input()
    if request_ == "exit":
        toexit = True
    elif request_ == "back":
        print_back()
    else:
        process_uri(dir, request_)
