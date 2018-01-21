"""
Google Books API
~~~~~~

This module provides a Google Books object which
    1. requests to list Books with string provided
    2. creates a library from json returned by request
    3. saves the library in csv format
    4. can sort the books by - price, avg rating, rating count, published date, page count
    5. reads the library from csv
    6. parses command line arguments to search and save the library to file or
    search, sort and save the library to file


Example Usage
~~~~~~~~~~~~~
Usage: booksapi.py [-h] [--search SEARCH] [--read READ] [--write WRITE]
                    [--sortby [{Published Date,Page Count,Price,Rating Count,Average Rating}]]
                    [--htol HTOL]

Search for Books from Google Books

Optional arguments:
  -h, --help            Show this help message and exit.
  --search SEARCH       string to search for in Google Books
  --read READ           read from CSV file
  --write WRITE         write to CSV file
  --sortby [{Published Date,Page Count,Price,Rating Count,Average Rating}]
                        sorts the library by sortby option
  --htol HTOL           True if high to low or False if low to high


"""

# see
#   http://docs.python-requests.org/en/v0.10.7/index.html
# install requests via:
#   /usr/local/share/python3/pip install requests

import json
import csv
from logging import error
import requests
import os, sys
import argparse


class GoogleBooks():
    def __init__(self):
        self.url = 'https://www.googleapis.com/books/v1/volumes'
        self.parms = {'q':''}
        self.search = ""

    def library(self, search):
        """
        constructs a library based on search string given
        :param search: search string
        :return obj: json object
        """
        self.parms['q'] = search
        response = requests.get(self.url, params=self.parms)
        print "Response Code: ", response.status_code

        # check if response status is 400
        if response.status_code != 200:
            error('Bad Request or Search string empty')
            exit(1)

        books = json.loads(response.text)
        return books

    def construct_data_from_json(self, books):
        """
        constructs raw data from json object with fields -
            "Book Title","Authors","Publisher","Published Date",
            "Page Count","Price","Rating Count","Average Rating"
        :param books: json object
        :return: list of book dictionaries
        """
        new_books=[]
        for k in books['items']:
            values = {"Book Title":"","Authors":"",
                      "Publisher":"", "Published Date":"",
                      "Page Count":"", "Price":"",
                      "Rating Count":"", "Average Rating":""}
            try:
                values["Book Title"] = k['volumeInfo']['title']
            except:
                pass
            try:
                values["Authors"] = ",".join([author for author in k['volumeInfo']['authors']])
            except:
                pass
            try:
                values["Publisher"] = k['volumeInfo']['publisher']
            except:
                pass
            try:
                values["Published Date"] = k['volumeInfo']['publishedDate']
            except:
                pass
            try:
                values["Page Count"] = k['volumeInfo']['pageCount']
            except:
                pass
            try:
                values["Price"] = str(k['saleInfo']['listPrice']['amount']) + " " + \
                        str(k['saleInfo']['listPrice']['currencyCode'])
            except:
                pass
            try:
                values["Rating Count"] = k['volumeInfo']['ratingsCount']
            except:
                pass
            try:
                values["Average Rating"] = k['volumeInfo']['averageRating']
            except:
                pass

            new_books.append(values)

        return new_books

    def write_to_csv(self, new_books, file):
        """
        write to csv file output.csv with fields -
            "Book Title","Authors","Publisher","Published Date",
            "Page Count","Price","Rating Count","Average Rating"
        :param new_books: list of book dictionaries
        :param file: file to write to
        """
        fo = open(file, "w")
        writeCSV = csv.writer(fo)
        header = ["Book Title","Authors","Publisher","Published Date",
                  "Page Count","Price","Rating Count","Average Rating"]
        writeCSV.writerow(header)

        for k in new_books:
            title = k["Book Title"]
            authors = k["Authors"]
            publisher = k["Publisher"]
            published_date = k["Published Date"]
            page_count = k["Page Count"]
            price= k["Price"]
            rating_count = k["Rating Count"]
            avg_count = k["Average Rating"]
            values = [title, authors, publisher, published_date, page_count, price, rating_count, avg_count]
            writeCSV.writerow(values)
        fo.close()

    def read_from_csv(self, file):
        """
        read library data from csv file
        :param file: file to read from
        """
        try:
            with open(file) as fr:
                readCSV = csv.reader(fr, delimiter=',')
                for row in readCSV:
                    print(",".join(row))
                fr.close()
        except IOError:
            error("File {} not found in path {}".format(file, os.curdir))
            exit(1)

    def sort(self, books, sortby, ascending):
        """
        sort list of book dictionaries by sortby param
        sortby param - price, avg rating, rating count, published date, page count
        :param books: list of book dictionaries
        :param sortby: str param
        :return: list of book dictionaries
        """
        sortedBooks = sorted(books, key=lambda k: k[sortby], reverse=ascending)
        return sortedBooks

    def construct_library(self, args):
        """
        constructs library
        :param args: Parser arguments
        :return:
        """
        if args.search is None:
            self.search = input("Enter the search string to search for in Google books: \n")
        else:
            self.search = args.search

        if args.sortby is None:
            books = self.library(self.search)
            new_books = self.construct_data_from_json(books)
            self.write_to_csv(new_books, args.write)
            self.read_from_csv(args.write)
        else:
            books = self.library(self.search)
            new_books = self.construct_data_from_json(books)
            sort_books = self.sort(new_books, args.sortby, args.hightolow)
            self.write_to_csv(sort_books, args.write)
            self.read_from_csv(args.write)


def create_parser(args):
    parser = argparse.ArgumentParser(description='Search for Books from Google Books')

    sortby_options = ["Published Date", "Page Count", "Price", "Rating Count", "Average Rating"]

    parser.add_argument("--search",
                        help="string to search for in Google Books",
                        required=False, default=None)
    parser.add_argument("--read", help="read from CSV file",
                        required=False, default="output.csv")
    parser.add_argument("--write", help="write to CSV file",
                        required=False, default="output.csv")
    parser.add_argument("--sortby", help="sorts the library by sortby option", choices=sortby_options,
                        required=False, nargs='?', default=None)
    parser.add_argument("--htol", help="True if high to low or False if low to high",
                        type=bool, required=False, default=False)

    # try:
    args = parser.parse_args()
    print "Args: ", args
    bk = GoogleBooks()
    bk.construct_library(args)
    # except:
    #     parser.print_help()

def main():
    create_parser(sys.argv[1:])

if __name__ == '__main__':
    main()
