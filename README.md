# booksapi
Lists and sorts library data from google books api

Google Books API
~~~~~~~~~~~~~~~~~~
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

    
   
