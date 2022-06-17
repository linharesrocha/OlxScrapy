# Imports
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas as pd
import time


def creating_links():
    for i in range(count, stop):
        all_urls.append('https://mg.olx.com.br/belo-horizonte-e-regiao?o=' + str(i) + '&q=' + pesquisa)


def scrapy_data():
    # Scraping Data in each URL
    for url in all_urls:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        page_soup = BeautifulSoup(webpage, 'html.parser')

        # Container
        container = page_soup.find(id='ad-list')

        # Check if there is an anuncio
        try:
            # Each product is in a list
            products = container.find_all('li')

            # Break if there are no products from today or yesterday
            if 'Hoje' not in str(products) and 'Ontem' not in str(products):
                break

            for product in products:
                # Ignoring afs-search
                try:
                    name = product.find('a', attrs={"target": "_blank"}).get("title")
                    link = product.find('a', attrs={"target": "_blank"}).get("href")
                    price = product.find('span',
                                         attrs={"aria-label": True, "title": False, "class": True, "color": "dark",
                                                "font-weight": "400"}).getText().replace('R$ ', '').replace('.', '')
                    date_publication = product.find_all('span',
                                                        attrs={"aria-label": True, "title": False, "color": "dark",
                                                               "font-weight": "400"})[-1].getText()

                    list_date.append(date_publication)
                    list_price.append(price) if price != '' else list_price.append(0)
                    list_name.append(name)
                    list_link.append(link)
                except:
                    continue
        # If there are no more ads
        except Exception as e:
            print(str(e))
            break;


def save_data():
    # Dictionary of Lists
    dictionary = {'nome': list_name, 'preco': list_price, 'data_publicacao': list_date, 'link': list_link}

    # Creating a Dataframe
    df = pd.DataFrame(dictionary)

    # Creating column index
    df['ordem_publicacao'] = df.index

    # Transformation
    df['preco'] = df['preco'].astype(float)

    # Sorting by Price
    df.sort_values(by=['preco', 'ordem_publicacao'], ascending = [True, True], inplace=True)

    # Converting to Excel
    writer = pd.ExcelWriter('/home/guilherme/Desktop/data.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Olx', index=False)
    for column in df:
        column_length = max(df[column].astype(str).map(len).max(), len(column))
        col_idx = df.columns.get_loc(column)
        writer.sheets['Olx'].set_column(col_idx, col_idx, column_length)
    writer.save()

if __name__ == '__main__':
    # Start mesure Execution Time
    st = time.time()

    # Creating Lists
    list_name = []
    list_price = []
    list_link = []
    list_date = []
    all_urls = []
    list_sort = []

    # Counting
    count = 1
    count_sort = 1
    stop = 50

    # User Search
    pesquisa = input('O que você deseja pesquisar? ').replace(' ', '+')

    # Functions
    creating_links()
    scrapy_data()
    save_data()


    # Finish measure Execution Time
    elapsed_time = time.time() - st
    print('Execution time:', time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
