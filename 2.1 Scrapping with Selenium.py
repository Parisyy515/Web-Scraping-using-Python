# Resources:

# Chrome Web-driver Download:
# https://sites.google.com/a/chromium.org/chromedriver/downloads

# Selenium Documentation:
# https://selenium-python.readthedocs.io/

# book:
# https://scholar.harvard.edu/files/tcheng2/files/selenium_documentation_0.pdf


##############################################################################
from selenium import webdriver
from selenium.webdriver.support.select import Select

# load password into a variable
pw = input("Please type pw ")

# setting up driver - download chrome driver and place it on your local directory, supply the path below. Chrome driver download - https://sites.google.com/a/chromium.org/chromedriver/downloads
PATH = "/Users/zhengguo/chromedriver"
driver = webdriver.Chrome(PATH)

# provide the web page you would like to scrap from
driver.get("https://thebellydancebundle.com/wp-login.php")

# work on username
username = driver.find_element_by_id("user_login")
username.clear()
username.send_keys("pariseasterday@gmail.com")

# work on password
password = driver.find_element_by_name("pwd")
password.clear()
password.send_keys(pw)

# work on the login button, right-click "inspect" on the target element, then right-click copy XPath on the corresponding source code. (Xpath content will be copied) 
driver.find_element_by_xpath("//*[@id='wp-submit']").click()

# print out content text format
print(driver.find_element_by_id("queryResultsForm").text)

##############################################################################
# Example: work on gender selection button
obj = Select(driver.find_element_by_name("optSexCode"))
if Gender == 'M':
    obj.select_by_index(2)
elif Gender == 'F':
    obj.select_by_index(1)
else:
    obj.select_by_index(3)

# Example: work on scrape table, when identified by odd and even rows
even = driver.find_elements_by_class_name("evenRow")
odd = driver.find_elements_by_class_name("oddRow")
o = []
e = []

for value in odd:
    o.append(value.text)
for value in even:
    e.append(value.text)

length = len(o)
i = 0
al = []

while i < length:
    al.append(e[i])
    al.append(o[i])
    i = i+1
