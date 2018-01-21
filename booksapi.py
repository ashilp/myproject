"""
Google Books API
~~~~~~

This module provides a Google Books object which
    1. requests to list Books with string provided
    2. creates a library from json returned by request
    3. saves the library in csv format
    4. can sort the books by - price, avg rating, rating count, published date, page count
       in ascending or descending order
    5. parses command line arguments to search, sort and save the library to file
    6. loads the library data to console from CSV


Example Usage
~~~~~~~~~~~~~
Usage: booksapi.py [-h] [--search SEARCH] [--file FILE] [--loadCSV LOADCSV]
                   [--sortby [{Published Date,Page Count,Price,Rating Count,Average Rating}]]
                   [--htol HTOL]

Search for Books from Google Books

Optional arguments:
  -h, --help            Show this help message and exit.
  --search SEARCH       string to search for in Google Books
  --file FILE           CSV file to read and write to
  --loadCSV LOADCSV     loads CSV file
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
        print "Writing to file: ", file
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
                print "Reading from file: ", file
                readCSV = csv.reader(fr, delimiter=',')
                for row in readCSV:
                    print(",".join(row))
                fr.close()
        except IOError:
            error("File {} not found in path {}".format(file, os.getcwd()))
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
            self.search = raw_input("Enter the search string to search for in Google books: \n")
        else:
            self.search = args.search

        books = self.library(self.search)
        new_books = self.construct_data_from_json(books)
        if args.sortby is None:
            # --search, --search --file, "",--search --htol,
            # --search --file --htol
            self.write_to_csv(new_books, args.file)
        else:
            # --search --sortby,--search --sortby --htol,
            # --search --sortby --file, --search --sortby --file --htol
            sort_books = self.sort(new_books, args.sortby, args.htol)
            self.write_to_csv(sort_books, args.file)

        if args.loadCSV:
            self.read_from_csv(args.file)


def create_parser(args):
    parser = argparse.ArgumentParser(description='Search for Books from Google Books')

    sortby_options = ["Published Date", "Page Count", "Price", "Rating Count", "Average Rating"]

    parser.add_argument("--search",
                        help="string to search for in Google Books",
                        required=False, default=None)
    parser.add_argument("--file", help="CSV file to read and write to",
                        required=False, default="output.csv")
    parser.add_argument("--loadCSV", help="loads CSV file",
                        type=bool, required=False, default=True)
    parser.add_argument("--sortby", help="sorts the library by sortby option", choices=sortby_options,
                        required=False, nargs='?', default=None)
    parser.add_argument("--htol", help="True if high to low or False if low to high",
                        type=bool, required=False, default=False)

    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        exit(1)

    print "Args: ", args
    bk = GoogleBooks()
    bk.construct_library(args)

def main():
    create_parser(sys.argv[1:])

if __name__ == '__main__':
    main()
