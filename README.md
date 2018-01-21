# booksapi
Lists and sorts library data from google books api

Google Books API
~~~~~~

This module provides a Google Books object which
    1. makes a request to list Books with string provided
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
