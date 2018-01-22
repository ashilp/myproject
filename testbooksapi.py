"""
Testing Google Books API
~~~~~~

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

"""


import unittest
import booksapi
import sys, os, csv
import logging

logging.basicConfig(level=logging.INFO)


class TestBooksApi(unittest.TestCase):
    def setUp(self):
        pass

    def test_search(self):
        """
        search for string "news" should give appropriate results
        """
        result, reason = search_result("news")
        logging.info(reason)
        self.assertEquals(result, 'Pass', msg=reason)

    def test_search_with_spaces(self):
        """
        search for string "White Elephant" should give appropriate results
        """
        result, reason = search_result("White Elephant")
        logging.info(reason)
        self.assertEquals(result, 'Pass', msg=reason)

    def test_search_with_spaces_doesnt_work(self):
        """
        search for string "New York" should give appropriate results
        as "New York" does not match one of the book titles returned by google search api, test fails
        """
        result, reason = search_result("New York")
        logging.info(reason)
        self.assertEquals(reason, 'Book title `Americanah` does not have search string `New York`')

    def test_search_random_string(self):
        """
        search for string "sdfghjrt" should give appropriate results
        test caught the case where the api does not handle when the search results are empty
        """
        result, reason = search_result("sdfghjrt")
        logging.info(reason)
        self.assertEquals(result, 'Pass', msg=reason)

    def test_search_with_one_character(self):
        """
        search for string "u" should give appropriate results
        """
        result, reason = search_result("u")
        logging.info(reason)
        self.assertEquals(result, 'Pass', msg=reason)

    def test_search_with_empty_string(self):
        """
        search for empty string should result in Bad Request
        """
        try:
            result, reason = search_result("")
        except SystemExit, e:
            logging.info("Bad request or Search string not given")
            self.assertEquals(str(e),'1',"Bad Request did not occur")

    def test_search_sort_rating_count(self):
        """
        search for string `cat` should give results sorted by `Rating Count`
        """
        result, reason = search_sort_result("cat","Rating Count")
        logging.info(reason)
        self.assertEquals(result, 'Pass', msg=reason)

    def test_search_sort_average_rating(self):
        """
        search for string `cat` should give results sorted by `Average Rating`
        """
        result, reason = search_sort_result("cat","Average Rating")
        logging.info(reason)
        self.assertEquals(result, 'Pass', msg=reason)

    def test_search_sort_page_count(self):
        """
        search for string `cat` should give results sorted by `Page Count`
        """
        result, reason = search_sort_result("cat", "Page Count")
        logging.info(reason)
        self.assertEquals(result, 'Pass', msg=reason)

    def test_search_sort_price(self):
        """
        search for string `cat` should give results sorted by `Price`
        """
        result, reason = search_sort_result("cat", "Price")
        logging.info(reason)
        self.assertEquals(result, 'Pass', msg=reason)

    def test_search_sort_published_date(self):
        """
        search for string `news` should give results sorted by `Published Date`
        """
        result, reason = search_sort_result("news", "Published Date")
        logging.info(reason)
        self.assertEquals(result, 'Pass', msg=reason)

    def test_search_sort_price_htol(self):
        """
        search for string `cat` should give results sorted by `Page Count` in descending order
        """
        result, reason = search_sort_result("cat", "Price", "True")
        logging.info(reason)
        self.assertEquals(result, 'Pass', msg=reason)

    def test_search_sort_wrong(self):
        """
        search for string `cat` should prompt for wrong sort option
        """
        try:
            result, reason = search_sort_result("cat", "price", "True")
        except SystemExit, e:
            logging.info("Sort option passed not found among sort options available")
            self.assertEquals(str(e),'1',"Wrong Sort Order not raised")


def search_sort_result(string, sortby, htol = False):
    """
    searches for `string` in book titles and checks if results are sorted by `sortby` option
    in ascending or descending order
    :param string: string to search in booktitles
    :param sortby: sort the library by sortby
    :param htol: ascending if htol is False else descending
    :return: Pass or Fail, msg
    """
    sys.argv[1:] = ['--search', string, '--sortby', sortby, '--htol', htol]
    # writes to output.csv by default
    booksapi.create_parser(sys.argv[1:])
    obj = read_CSV()
    if isinstance(obj, list):
        logging.debug("Object Returned is list")
        if not obj:
            #handles the case when list is empty
            result, msg = "Pass", "No results returned by search " + string
        else:
            #checks if string present in book title
            result, msg = compare(obj, string)
            #if string present in book title, checks if library is sorted by sortby param
            if result == 'Pass':
                result, msg = isSorted(obj, sortby, htol)
        return result, msg
    elif isinstance(obj, str):
        return "Fail", obj


def search_result(string):
    """
    searches for `string` in book titles
    :param string: string to search in booktitles
    """
    sys.argv[1:] = ['--search', string]
    # writes to output.csv by default
    booksapi.create_parser(sys.argv[1:])
    obj = read_CSV()
    if isinstance(obj, list):
        logging.debug("Object Returned is list")
        if not obj:
            # handles the case when list is empty
            result, msg = "Pass", "No results returned by search "+string
        else:
            # checks if string present in book title
            result, msg = compare(obj, string)
        return result, msg
    elif isinstance(obj, str):
        return "Fail", obj


def compare(booklist, search_str):
    """
    compares if search string is present title of each book
    :param booklist: list of book dictionaries
    :param search_str: string to search for in book title
    :return: Pass or Fail, message
    """
    for b in booklist:
        if search_str.lower() not in b["Book Title"].lower():
            msg = "Book title `{}` does not have search string `{}`".format(b["Book Title"], search_str)
            return "Fail", msg
    return "Pass", search_str + " present in book title"


def isSorted(booklist, sortby, htol):
    """
    checks if the library is sorted by `sortby` option in ascending or descending order
    :param booklist: list of book dictionaries
    :param sortby: sort the library by sortby
    :param htol: ascending if htol is False else descending
    :return: Pass or Fail, message
    """
    #extracts the column sortby from library
    tmplist=[b[sortby] for b in booklist if b[sortby]]
    order = "descending" if htol else "ascending"
    logging.debug("Sorted List of `{}` is `{}`".format(sortby, " ".join(tmplist)))
    if sortby=="Published Date":
        sortby_list = sorted(tmplist, key=lambda d: map(int, d.split('-')), reverse=htol)
        if sortby_list==tmplist:
            tmp_res = True
        else:
            tmp_res = False
    else:
        sortby_list = map(float, tmplist)
        if htol:
            tmp_res = all(sortby_list[i] >= sortby_list[i + 1] for i in xrange(len(sortby_list) - 1))
        else:
            tmp_res = all(sortby_list[i] <= sortby_list[i + 1] for i in xrange(len(sortby_list) - 1))

    if tmp_res:
        msg = "Books are sorted by {} in {} order".format(sortby, order)
        return ("Pass", msg)
    else:
        msg = "Books are not sorted by {} in {} order".format(sortby, order)
        return ("Fail", msg)


def read_CSV(readfile="output.csv"):
    """
    reads from CSV file and converts it into object
    :param readfile: file to read from
    """
    try:
        with open(readfile) as fr:
            logging.info("Reading from file: {}".format(readfile))
            readCSV = csv.reader(fr, delimiter=',')
            books = []
            count = -1
            for row in readCSV:
                count+=1
                if count==0:
                    continue
                values = {"Book Title":row[0], "Authors": row[1],
                          "Publisher": row[2], "Published Date": row[3],
                          "Page Count": row[4], "Price": row[5],"Currency Code": row[6],
                          "Rating Count": row[7], "Average Rating": row[8]}
                books.append(values)
            fr.close()
        return books
    except IOError:
        return "File {} not found in path {}".format(readfile, os.getcwd())

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBooksApi)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print "---- START OF TEST RESULTS"
    print result
    print "result::errors"
    print result.errors
    print "result::failures"
    print result.failures
    print "result::skipped"
    print result.skipped
    print "result::successful"
    print result.wasSuccessful()
    print "result::test-run"
    print result.testsRun
    print "---- END OF TEST RESULTS"