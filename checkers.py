from bs4 import BeautifulSoup as BS
import helium

import requests
import time


def thriftys(item):
    headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        }
    # Get search page and pass into Beautiful Soup object
    thrifty = requests.get('https://www.thriftyfoods.com/search?k=' + item, headers=headers).content
    soup_thrift = BS(thrifty, 'html.parser')

    # Check for no results found, and return only empty search message if found
    if soup_thrift.find(id="body_0_main_1_NoResult_NoResultSentence"):
        brand = soup_thrift.find(id="body_0_main_1_NoResult_NoResultSentence").get_text(strip=True)
        name, unit, price = '', '', ''
    # Otherwise check for brand info, get item name, check for unit info, get price for first search result
    else:
        try:
            brand = soup_thrift.find(id="body_0_main_1_GrocerySearch_TemplateResult_SearchResultListView_ctrl0_ctl00_0_BrandNameZone_0").get_text(strip=True)
        except:
            brand = ''
        name = soup_thrift.find(class_="js-ga-productname").get_text(strip=True)
        try:
            unit = soup_thrift.find(id="body_0_main_1_GrocerySearch_TemplateResult_SearchResultListView_ctrl0_ctl00_0_SizeZone_0").get_text(strip=True)
        except:
            unit = ''
        price = soup_thrift.find('div', class_="item-product__price push-medium--bottom").get_text(strip=True)

    # Return info in a dictionary
    return {'brand': brand, 'name': name, 'unit': unit, 'price': price}

def superstore(item):
    # Get search page using chrome browser, wait for it to finish loading and pass to Beautiful Soup object
    browser = helium.start_chrome('https://www.realcanadiansuperstore.ca/search?search-bar=' + item, headless=True)
    time.sleep(2)
    soup_sstore = BS(browser.page_source, 'html.parser')

    # Check for no results found, and return only empty search message if found
    if soup_sstore.find(class_="search-no-results__section-title"):
        brand = soup_sstore.find(class_="search-no-results__section-title").get_text(strip=True)
        name, pack, unit, price = '', '', '', ''
    # Otherwise gather item info for first result
    else:
        brand = soup_sstore.find(class_="product-name__item product-name__item--brand").get_text(strip=True)
        name = soup_sstore.find(class_="product-name__item product-name__item--name").get_text(strip=True)
        pack = soup_sstore.find(class_="product-name__item product-name__item--package-size").get_text(strip=True)
        unit = soup_sstore.find(class_="price__unit selling-price-list__item__price selling-price-list__item__price--now-price__unit").get_text(strip=True)
        price = soup_sstore.find(class_="price selling-price-list__item__price selling-price-list__item__price--now-price").get_text(strip=True)

    # Return info in a dictionary
    return {'brand': brand, 'name': name, 'pack': pack, 'unit': unit, 'price': price}

def johns(item):
    # Site is identical to Superstore
    browser = helium.start_chrome('https://www.yourindependentgrocer.ca/search?search-bar=' + item, headless=True)
    time.sleep(2)
    soup_johns = BS(browser.page_source, 'html.parser')

    if soup_johns.find(class_="search-no-results__section-title"):
        brand = soup_johns.find(class_="search-no-results__section-title").get_text(strip=True)
        name, pack, unit, price = '', '', '', ''
    else:
        brand = soup_johns.find(class_="product-name__item product-name__item--brand").get_text(strip=True)
        name = soup_johns.find(class_="product-name__item product-name__item--name").get_text(strip=True)
        pack = soup_johns.find(class_="product-name__item product-name__item--package-size").get_text(strip=True)
        unit = soup_johns.find(class_="price__unit selling-price-list__item__price selling-price-list__item__price--now-price__unit").get_text(strip=True)
        price = soup_johns.find(class_="price selling-price-list__item__price selling-price-list__item__price--now-price").get_text(strip=True)

    return{'brand': brand, 'name': name, 'pack': pack, 'unit': unit, 'price': price}

def quality_foods(item):
    # Get search page and pass into Beautiful Soup object
    qf = requests.get('https://www.qualityfoods.com/search/default.aspx?keyword=' + item + '&sale=False&bonus=False&category=Any').content
    soup_qf = BS(qf, 'html.parser')
    # Grab all product td's
    qf_td = soup_qf.find_all('td', class_='product_listViewTD')

    # If there are more than 4 td's, search was not empty
    if len(qf_td) > 4:
        # Get spans and remove tag contents
        spn = qf_td[1].find('span')
        spn.clear()
        # Gather info
        name = qf_td[1].get_text(strip=True)
        unit = qf_td[2].get_text(strip=True)
        price = qf_td[4].get_text(strip=True)
    # Otherwise just get empty search message
    else:
        name = soup_qf.find(id="bodyContainerPlaceHolder_bodyPlaceHolder_noItemsPanel").get_text(strip=True)
        unit, price = '', ''

    # Return info in a dictionary
    return {'name': name, 'unit': unit, 'price': price}