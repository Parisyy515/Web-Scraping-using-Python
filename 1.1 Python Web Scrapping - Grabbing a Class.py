import bs4
import lxml
import requests

# First get the request
res = requests.get('https://en.wikipedia.org/wiki/Grace_Hopper')

# Create a soup from request, using lxml to decipher it
soup = bs4.BeautifulSoup(res.text, "lxml")

# check out the soup - entire content from the page
soup

# call for class "toctext"
soup.select(".toctext")

# assign first item into first_item
first_item = soup.select('.toctext')[0]

# grab the text attribute from this call
first_item.text

# loop through the class in the soup and print out each one
for item in soup.select(".toctext"):
    print(item.text)
