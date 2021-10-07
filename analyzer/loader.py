#!python3

FILE_PATH = './coins.txt'


class Loader:
    def __init__(self):
        print("Loader started")

    def get_coin_list():

        coin_list = open(FILE_PATH, 'r').read()
        return coin_list
