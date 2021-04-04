from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest


def get_titles_from_search_results(filename):

    """
    Write a function that creates a BeautifulSoup object on "search_results.htm". Parse
    through the object and return a list of tuples containing book titles (as printed on the Goodreads website) 
    and authors in the format given below. Make sure to strip() any newlines from the book titles and author names.

    [('Book title 1', 'Author 1'), ('Book title 2', 'Author 2')...]
    """
    with open(filename) as fp:
        soup = BeautifulSoup(fp, "html5lib")
    #print(soup)
    
    tags_title = soup.find_all('a',class_='bookTitle') 
    tags_author = soup.find_all('a',class_='authorName')
    collect_titles = []
    for tag in tags_title:
        info = tag.text.strip()
        collect_titles.append(info)
    #print(collect_titles) 

    collect_authors = []
    for tag in tags_author:
        info = tag.text.strip()
        collect_authors.append(info)
    #print(collect_authors) 

    l_of_tup =[]
    for i in range(len(collect_titles)):
        tup = (collect_titles[i],collect_authors[i])
        l_of_tup.append(tup)
    
    return l_of_tup


#get_titles_from_search_results("search_results.htm")

def get_search_links():
    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
    URLs for each of the first ten books in the search using the following format:

    ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]

    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to 
    your list, and , and be sure to append the full path to the URL so that the url is in the format 
    “https://www.goodreads.com/book/show/kdkd".

    """

    url = "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    tags = soup.find_all('a', class_='bookTitle')
    titles = []
    for tag in tags:
        info = tag.get('href')
        titles.append('https://www.goodreads.com' + str(info))
    
    return titles[:10]

#get_search_links()

def get_book_summary(book_url):
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the URL of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, and number 
    of pages. This function should return a tuple in the following format:

    ('Some book title', 'the book's author', number of pages)

    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title and number of pages.
    """
    r = requests.get(book_url)
    soup = BeautifulSoup(r.content, 'html.parser')

    title = soup.find('h1', id='bookTitle')
    t_info = title.text.strip()
    #print(t_info)

    author = soup.find('span', itemprop ='name')
    a_info = author.text.strip()
    #print(a_info)

    pages = soup.find('span', itemprop ='numberOfPages')
    p1_info = pages.text.strip()
    p_info = p1_info.replace(" pages", "")
    p_inf = int(p_info)
    #print(type(p_inf))

    return (t_info,a_info,p_info)

#get_book_summary('https://www.goodreads.com/book/show/4667024-the-help') 


def summarize_best_books(filepath):
    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2020"
    page in "best_books_2020.htm". This function should create a BeautifulSoup object from a 
    filepath and return a list of (category, book title, URL) tuples.
    
    For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should append 
    ("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2020") 
    to your list of tuples.
    """
    with open(filepath) as fp:
        soup = BeautifulSoup(fp, "html5lib")
    #print(soup)

    categories = soup.findall('h4',class_ = "category__copy")
    titles = soup.findall('a',class_ = "readable")
    urls = soup.findall('a',class_ = "readable")
    
    l_titles = []
    for t in titles:
        l_titles.append(t.text)
    
    l_categories = []
    for c in categories:
        l_categories.append(c.text)

    l_urls = []
    for u in urls:
        l_urls.append(u.text)

    l_tups = []
    for i in range(len(l_titles)):
        l_tups.append((l_categories[i],l_titles[i],l_urls[i]))

    return l_tups


    

#summarize_best_books('best_books_2020.htm')


def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_titles_from_search_results()), writes the data to a 
    csv file, and saves it to the passed filename.

    The first row of the csv should contain "Book Title" and "Author Name", and
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Book title,Author Name
    Book1,Author1
    Book2,Author2
    Book3,Author3
    ......

    This function should not return anything.
    """
     
    fields = ['Book Title', 'Author Name']
 
    with open(filename, 'w') as csvfile:  
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerow(fields) 
        csvwriter.writerows(list(data))

    #fh = open(filename)
    #f = fh.read()
    #print(f)

#write_csv([('HP','jk rowling'),('LOTR', 'tolken')],'books.csv')


def extra_credit(filepath):
    """
    EXTRA CREDIT

    Please see the instructions document for more information on how to complete this function.
    You do not have to write test cases for this function.
    """
    pass

class TestCases(unittest.TestCase):

    # call get_search_links() and save it to a static variable: search_urls
    search_urls = get_search_links()


    def test_get_titles_from_search_results(self):
        # call get_titles_from_search_results() on search_results.htm and save to a local variable
        titleauthor_tups = get_titles_from_search_results('search_results.htm')

        # check that the number of titles extracted is correct (20 titles)
        self.assertEqual(len(titleauthor_tups), 20)

        # check that the variable you saved after calling the function is a list
        self.assertIsInstance(titleauthor_tups, list)

        # check that each item in the list is a tuple
        for tup in titleauthor_tups:
            self.assertIsInstance(tup, tuple)

        # check that the first book and author tuple is correct (open search_results.htm and find it)
        self.assertEqual(titleauthor_tups[0], ('Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'))

        # check that the last title is correct (open search_results.htm and find it)
        self.assertEqual(titleauthor_tups[-1], ('Harry Potter: The Prequel (Harry Potter, #0.5)', 'Julian Harrison'))

    def test_get_search_links(self):
        # check that TestCases.search_urls is a list
        self.assertIsInstance(TestCases.search_urls, list)

        # check that the length of TestCases.search_urls is correct (10 URLs)
        self.assertEqual(len(TestCases.search_urls), 10)

        # check that each URL in the TestCases.search_urls is a string
        for url in TestCases.search_urls:
            self.assertIsInstance(url, str)

        # check that each URL contains the correct url for Goodreads.com followed by /book/show/
        for url in TestCases.search_urls: 
            self.assertIn('https://www.goodreads.com/book/show/',url)

    def test_get_book_summary(self):
        # create a local variable – summaries – a list containing the results from get_book_summary()
        # for each URL in TestCases.search_urls (should be a list of tuples)
        summaries = []
        for url in TestCases.search_urls:
            sm = get_book_summary(url)
            summaries.append(sm)

        # check that the number of book summaries is correct (10)
        self.assertEqual(len(summaries), 10)

            # check that each item in the list is a tuple
        for item in summaries:
            self.assertIsInstance(item,tuple)

            # check that each tuple has 3 elements
        for item in summaries:
            self.assertEqual(len(item),3)

            # check that the first two elements in the tuple are string
        for item in summaries:
            self.assertIsInstance(titem[0],str)
        for item in summaries:
            self.assertIsInstance(item[1],str)

            # check that the third element in the tuple, i.e. pages is an int
        for item in summaries:
            self.assertIsInstance(type(item[2]),int)
        
            # check that the first book in the search has 337 pages
        self.assertEqual(summaries[0][2],337)

    def test_summarize_best_books(self):
        # call summarize_best_books and save it to a variable
        bb_tup_lst = summarize_best_books("best_books_2020.htm")

        # check that we have the right number of best books (20)
        self.assertEqual(len(bb_tup_lst),20)

            # assert each item in the list of best books is a tuple
        for item in bb_tup_lst:
            assertIsInstance(item,tuple)
            # check that each tuple has a length of 3
        for item in bb_tup_lst:
            assertEqual(len(item),3)
        # check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'
        for item in bb_tup_lst:
            assertEqual(bb_tup_lst[0],('Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'))

        # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'
        for item in bb_tup_lst:
            assertEqual(bb_tup_lst[0],('Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'))

    def test_write_csv(self):
        # call get_titles_from_search_results on search_results.htm and save the result to a variable
        ta_list = get_titles_from_search_results('search_results.htm')

        # call write csv on the variable you saved and 'test.csv'
        write_csv(ta_list,'test.csv')

        # read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)
        with open('test.csv', newline='') as f:
            csv_lines = csv.reader(f)
            for line in csv_lines:
                print(line)

        # check that there are 21 lines in the csv
        self.assertEqual(len(csv_lines),21)

        # check that the header row is correct
        self.assertIs(csv_lines[0],'Book Title', 'Author Name')

        # check that the next row is 'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'
        self.assertIs(csv_lines[1],'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling')

        # check that the last row is 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'
        self.assertIs(csv_lines[-1],'Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling')


if __name__ == '__main__':
    print(extra_credit("extra_credit.htm"))
    unittest.main(verbosity=2)



