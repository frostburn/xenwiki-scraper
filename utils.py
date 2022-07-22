from bs4 import BeautifulSoup

Soup = lambda fp: BeautifulSoup(fp, features='lxml')
