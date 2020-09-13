#dependencies
from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
import pandas as pd

#create function scrape

def scrape():

    #define dictionary to hold everything in Python
    mars_dict = {}

    #parsing to obtain title of news and paragraphs
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    #parsing to find news titles
    results = soup.find_all('div', class_='content_title')
    for result in results:
        news_title = result.find('a').text
    
        mars_dict['news_title'] = news_title

    #parsing to find article's text
    res3 = soup.find_all('div', class_='rollover_description_inner')
    for res in res3:
        n_p = res.text
    
        mars_dict['news_paragraph'] = n_p

    #connection to splinter
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    #url for images
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    #finding url for featured image
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    url = soup.find('a', class_="button fancybox").get('data-fancybox-href').strip()
    featured_image_url = 'https://www.jpl.nasa.gov' + url
    mars_dict['featured_image_url'] = featured_image_url

    #provide URL to find table
    url_table = 'https://space-facts.com/mars/'

    #show all tables available
    tables = pd.read_html(url_table)
    tables

    #choose and transform chosen table
    mars_df = tables[0]
    mars_df.columns = ['Facts','Values']
    mars_df.set_index('Facts', inplace=True)
    mars_df

    #export to html
    html_table = mars_df.to_html()
    mars_dict['html_table'] = html_table

    #url to find images with splinter
    url_images = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_images)

    #get all links to images pages
    html_5 = browser.html
    soup_43 = BeautifulSoup(html_5, 'html.parser')
    hem_img_url = []
    links = soup_43.find_all('h3')
    l_txt = []
    for link in links:
        link_text = link.text
        l_txt.append(link_text)
    print(l_txt)

    #get Cerberus information
    dict_Cerberus = {}
    browser.click_link_by_partial_text(l_txt[0])
    html_Cerberus = browser.html
    soup_Cerberus = BeautifulSoup(html_Cerberus, 'html.parser')
    linkCerberus = soup_Cerberus.find('div', class_="downloads").find('a').get("href")
    linkCerberus

    #Append to dictionary
    dict_Cerberus["title"]=l_txt[0]
    dict_Cerberus["img_url"]=linkCerberus

    #return to main page
    url_images = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_images)
    html_5 = browser.html
    soup_43 = BeautifulSoup(html_5, 'html.parser')

    #get Schiaparelli information
    dict_Schiaparelli = {}
    browser.click_link_by_partial_text(l_txt[1])
    html_Schiaparelli = browser.html
    soup_Schiaparelli = BeautifulSoup(html_Schiaparelli, 'html.parser')
    linkSchiaparelli = soup_Schiaparelli.find('div', class_="downloads").find('a').get("href")
    linkSchiaparelli

    #append to dictionary
    dict_Schiaparelli["title"]=l_txt[1]
    dict_Schiaparelli["img_url"]=linkSchiaparelli

    #return to main page
    url_images = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_images)
    html_5 = browser.html
    soup_43 = BeautifulSoup(html_5, 'html.parser')

    #get Syrtis information
    dict_Syrtis = {}
    browser.click_link_by_partial_text(l_txt[2])
    html_Syrtis = browser.html
    soup_Syrtis = BeautifulSoup(html_Syrtis, 'html.parser')
    linkSyrtis = soup_Syrtis.find('div', class_="downloads").find('a').get("href")
    linkSyrtis

    #append to dictionary
    dict_Syrtis["title"]=l_txt[2]
    dict_Syrtis["img_url"]=linkSyrtis

    #return to main page
    url_images = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_images)
    html_5 = browser.html
    soup_43 = BeautifulSoup(html_5, 'html.parser')

    #get Valles information
    dict_Valles = {}
    browser.click_link_by_partial_text(l_txt[3])
    html_Valles = browser.html
    soup_Valles = BeautifulSoup(html_Valles, 'html.parser')
    linkValles = soup_Valles.find('div', class_="downloads").find('a').get("href")
    linkValles

    #append to dictionary
    dict_Valles["title"]=l_txt[3]
    dict_Valles["img_url"]=linkValles

    hem_img_url = []

    #append all dictionaries to list
    hem_img_url.append(dict_Cerberus)
    hem_img_url.append(dict_Schiaparelli)
    hem_img_url.append(dict_Syrtis)
    hem_img_url.append(dict_Valles)

    mars_dict['hem_img_url'] = hem_img_url

    return mars_dict