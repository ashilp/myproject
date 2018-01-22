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
    7. if search string option not given, it prompts for user input

Requirements
~~~~~~~~~~~~~

requests module:  pip install requests

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

Steps to Run App
~~~~~~~~~~~~~~~~~~

        >> cd  <Path to>/googlebooks_shilpa
        >> python booksapi.py --search 'cat' --sortby 'Price' --file '23andme.csv' --htol True --loadCSV True

        For output, refer to Example 1 in result_app.log

        >> python booksapi.py --file '23andme.csv' --loadCSV True

        For output, refer to Example 2 in result_app.log


#testbooksapi

Testing Google Books API
~~~~~~~~~~~~~~~~~~~~~~~~

This module covers the following test cases:
    1. search for a string `news` should give Book results whose title contains the string `news`
    2. search for string with spaces `White Elephant` should give Book results whose title contains the string `White Elephant`
    3. search for string `New York` should fail as the string does not match one of the book titles returned by google search api
    4. search for string "sdfghjrt" results in 0 results
    5. search for string with single character "u" should give Book results whose title contains the character `v`
    6. search for empty string should result in Bad Request
    7. search for string `cat` should give results sorted by `Rating Count` in ascending order
    8. search for string `cat` should give results sorted by `Average Rating` in ascending order
    9. search for string `cat` should give results sorted by `Page Count` in ascending order
    10. search for string `cat` should give results sorted by `Price` in ascending order
    11. search for string `news` should give results sorted by `Published Date` in ascending order
    12. search for string `cat` should give results sorted by `Page Count` in descending order
    13. search for string `cat` should prompt for wrong sort option when a sort option outside of
        "Published Date", "Page Count", "Price", "Rating Count", "Average Rating" is passed


Example Usage
~~~~~~~~~~~~~
Usage: testbooksapi.py

Steps to Run Automated Tests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        >> cd  <Path to>/googlebooks_shilpa
        >> python testbooksapi.py

        For output, refer to result_test.log

    
   
