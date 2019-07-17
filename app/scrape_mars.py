# import dependencies
# Same as Jup Notebook script
from splinter import Browser
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd

def scrape_all():
    executable_path = {'executable_path': 'C:\\Users\\jbpar\\Desktop\\git\\Mission_to_Mars\\chromedriver.exe'}
    browser = Browser('chrome', **executable_path)

    news_title, news_p = mars_news(browser)

    # For mongo, we're gonna have a dictionary
    data = {
        "news_title": news_title,
        "news_paragaph": news_p,
        "featured_image": featured_image(browser),
        "current_weather_on_mars": mars_weather(browser),
        "mars_facts": mars_facts(browser)
    }

    return data

def mars_news(browser): # Time to copy stuff over from the Pandas file!
    # Websizzle used for scraping
    url = 'https://mars.nasa.gov/news/'
    # Hey, driver! Go get it.
    browser.visit(url)
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
    # Open, visit, and scrape the proper site
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    # Need to see what's up with the "Full Image" button
    full_image_elem = browser.find_by_id('full_image')
    # CLICK the "Full Image" button
    full_image_elem.click()
    # Need to see what's up with the "More Info" button
    more_info = browser.find_link_by_partial_text('more info')
    # CLICK the "More Info" button
    more_info.click()
    # Make some Soup!
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')  
    # Traverse the CSS
    # <figure class="lede"> --> <a href = "blahblah"> --> <img alt/title/class="blah" src="WHAT WE WANT">
    img_url_rel = img_soup.select_one('figure.lede a img').get("src")
    #Create url by appending things to other things
    url_base = 'https://www.jpl.nasa.gov'
    img_url = f'{url_base}{img_url_rel}'

    return img_url

def mars_weather(browser):
    # Open, visit, and scrape the proper site
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    # Make some Soup!
    html = browser.html
    weather_soup = BeautifulSoup(html, 'html.parser')
    # With multiple instances of the same text, pull out the one easiest to edit
    temp_text = weather_soup.find_all('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")[1].text
    mars_weather = temp_text.replace("\n", ", ")
    
    return mars_weather

def mars_facts(browser):
    # Open, visit, and scrape the proper site
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    html = browser.html
    facts_soup = BeautifulSoup(html, 'html.parser')
    temp = pd.read_html('https://space-facts.com/mars/')[1]
    temp.rename(columns={0: 'Description', 1: 'Value'}, inplace=True)
    temp_two_electric_boogaloo = temp.set_index('Description')
    mars_facts = temp_two_electric_boogaloo.to_html(header=True, index=True)
    
    return mars_facts

def mars_hemispheres(browser):