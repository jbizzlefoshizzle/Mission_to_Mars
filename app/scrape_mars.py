# import dependencies
# Same as Jup Notebook script
from splinter import Browser
from bs4 import BeautifulSoup
from selenium import webdriver

def scrape_all():
    executable_path = {'executable_path': 'C:\\Users\\jbpar\\Desktop\\git\\Mission_to_Mars\\chromedriver.exe'}
    browser = Browser('chrome', **executable_path)

    news_title, news_p = mars_news(browser)

    # For mongo, we're gonna have a dictionary
    data = {
        "news_title": news_title,
        "news_paragaph": news_p,
        "featured_image": featured_image(browser)
    }

    return data

def mars_news(browser): # Time to copy stuff over from the Pandas file!
    # Websizzle used for scraping
    url = 'https://mars.nasa.gov/news/'
    # Hey, driver! Go get it.
    browser.visit(url)
    # driver.get(url)

    # If we have our elements
    # Now we can make our Soup
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        news_title = slide_elem.find('div', class_="content_title").get_text() # news_title FOUND!
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text() # news_p FOUND!
    except AttributeError:
        return None, None
    
    return news_title, news_p

def featured_image(browser):
    return img_url