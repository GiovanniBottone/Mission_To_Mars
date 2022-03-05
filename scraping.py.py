# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Set Up Splinter
# set your executable path in the next cell, then set up the URL for scraping
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Visit the Mars news Site
# assign the url and instruct the browser to visit it.
# With the following line, browser.is_element_present_by_css('div.list_text', wait_time=1), we are accomplishing two things.
# One is that we're searching for elements with a specific combination of tag (div) and attribute (list_text).
# Secondly, we're also telling our browser to wait one second before searching for components.
# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# Convert the browser html to a soup object
# set up the HTML parser
# slide_elem is our parent element, meaning this element holds all other elements within it.
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# To assign the title and summary text to variables.
# In this line of code, we chained .find onto our previously assigned variable, slide_elem.
# This means "This variable holds a ton of information, so look inside of that information to find this specific data."
# The data we're looking for is the content title, which we've specified by saying, "The specific data is in a <div /> with a class of 'content_title'."
slide_elem.find('div', class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
# we need to get just the text, and the extra HTML stuff isn't necessary.
# We've added something new to our .find() method here: .get_text().
# When this new method is chained onto .find(), only the text of the element is returned.
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Since there are only three buttons, and we want to click the full-size image button, using the HTML tag in our code
# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# With the new page loaded onto our automated browser, it needs to be parsed so we can continue and scrape the full-size image URL
# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# We'll use the image tag and class (<img />and fancybox-img) to build the URL to the full-size image.
# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# An img tag is nested within this HTML, so we've included it.
# .get('src') pulls the link to the image.
# What we've done here is tell BeautifulSoup to look inside the <img /> tag for an image with a class of fancybox-image. 
# Basically we're saying, "This is where the image we want lives—use the link that's inside these tags."

# If we look at our address bar in the webpage, we can see the entire URL up there already; we just need to add the first portion to our app.
# Add the base URL to our code
# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

# Instead of scraping each row, or the data in each <td />, we're going to scrape the entire table with Pandas' .read_html() function.
# At the top of your Jupyter Notebook, add import pandas as pd to the dependencies
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

# Let's break it down:
# df = pd.read_htmldf = pd.read_html('https://galaxyfacts-mars.com')[0] With this line, we're creating a new DataFrame from the HTML table. 
# The Pandas function read_html() specifically searches for and returns a list of tables found in the HTML. 
# By specifying an index of 0, we're telling Pandas to pull only the first table it encounters, or the first item in the list. 
# Then, it turns the table into a DataFrame.

# df.columns=['description', 'Mars', 'Earth'] Here, we assign columns to the new DataFrame for additional clarity.

# df.set_index('description', inplace=True) By using the .set_index() function, we're turning the Description column into the DataFrame's index.
# inplace=True means that the updated index will remain in place, without having to reassign the DataFrame to a new variable.

# Pandas also has a way to easily convert our DataFrame back into HTML-ready code using the .to_html() function.
df.to_html()

# Quit the Browser
browser.quit()
