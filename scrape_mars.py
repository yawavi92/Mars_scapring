from bs4 import BeautifulSoup as bs
import pymongo
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt


def scrape_all():
    #import Splinter and set the chrome drive path
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #save url and visit the page 
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    #create BeautifulSoup 
    html = browser.html
    soup = bs(html, "html.parser")

    #retrieve news title and article 
    title = soup.find('div', class_='content_title').text
    #collect Paragraph Text 
    new_p = soup.find('div', class_='article_teaser_body').text
    # Print title and paragraph
    print(title)
    print('------------------------------------------------------')
    print(new_p)

    #use splinter to click featured image 
    # save and visit the url
    url="https://spaceimages-mars.com/"
    browser.visit(url)

    # set the path
    xpath = "/html/body/div[1]/img"
    #bring the full resolution
    full = browser.find_by_xpath(xpath)
    image_ = full[0]
    image_.click()
    #create a beautiful object
    html = browser.html
    soup = bs(html, "html.parser")
    image_url = soup.find("img", class_="headerimage fade-in")["src"]
    #concatenate to find the image url
    featured_image_url = url + image_url
    featured_image_url

    #save the mars facts url and visit the page
    #set the URL
    url ="https://galaxyfacts-mars.com/"

    #Extract the Facts Table from the URL using pandas
    tables = pd.read_html(url)
    tables

    # set the columns in the dataframes
    mars_df = tables[1]
    mars_df.rename(columns ={0 :'Description', 1: 'Dimension'}, inplace = True)
    mars_df

    #convert the dataframe back to html format
    fact = mars_df.to_html('table table-striped th-align-left table-bordered')
    fact

    #Mars hemispheres
    url ="https://marshemispheres.com/"
    browser.visit(url)

    #create a beautiful object
    html = browser.html
    soup = bs(html, "html.parser")

    # Extract the hemisphere element
    results = soup.find("div", class_="collapsible results")
    hemispheres = results.find_all("div", class_="item")

    #create the list to store the image urls
    hemisphere_image_urls=[]

    #Iterate trough each image
    for hemisphere in hemispheres :
    # Scrape the titles
        title = hemisphere.find("h3").text
    
    # the hem links
        link = hemisphere.find("a")["href"]
        url ="https://marshemispheres.com/"
        hem_link = url + link    
        browser.visit(hem_link)
    
    # Parse link HTMLs with Beautiful Soup
        fact = browser.html
        soup = bs(fact, "html.parser")
        print(soup.prettify())
    # Scrape the full size images
        load = soup.find("div", class_="downloads")
        load_url = load.find("a")["href"]
    
    # Add URLs and Titles 
        hemisphere_image_urls.append({"title": title, "image_url": url + load_url})

        
     # Create dictionary for all info scraped from sources above
    mars={
        "title":title,
        "paragraph":new_p,
        "featured_image":featured_image_url,
        "facts":fact,
        "hemispheres":hemisphere_image_urls,
        "last_modified": dt.datetime.now()
    }
        # Close the browser after scraping
    browser.quit()
    return mars