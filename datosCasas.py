import requests
from bs4 import BeautifulSoup
import pandas as pd
def crawl_web(seed_url, max_pages):
    pages_visited = 0
    pages_to_visit = [seed_url]
    visited_links = set()
    data = []
    while pages_visited < max_pages and pages_to_visit:
        url = pages_to_visit.pop(0)
        if url not in visited_links:
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    # Parse the HTML content
                    soup = BeautifulSoup(response.text, 'html.parser')
                    # Find all elements with class 'listing listing-card item'
                    listings = soup.find_all('div', class_='listing listing-card item')
                    cont = 0
                    # Iterate over each listing and print its text
                    for listing in listings:
                        cont=cont+1
                        title_element = listing.find('div', class_='listing-card__title')
                        title = title_element.text.strip() if title_element else 'N/A'

                        location_element = listing.find('div', class_='location__text')
                        location = location_element.text.strip() if location_element else 'N/A'

                        price_element = listing.find('div', class_='price')
                        price = price_element.text.strip() if price_element else 'N/A'

                        #detalles de la ventada de la casa
                        #things_element = listing.find('div', class_='item__content--description')
                        #morethings= things_element.text.strip() if things_element else 'N/A'

                       # more_element = listing.find('div', class_='item__content--information--links')
                       # moreInfo = more_element.text.strip() if more_element else 'N/A'


                       # Obtener las propiedades del listado
                        properties = [prop.find('div', class_='property__number').text.strip() for prop in listing.find_all('div', class_='property')]
                        # Asegurarse de que siempre haya suficientes propiedades
                        while len(properties) < 3:
                            properties.append('N/A')

                        # Crear el diccionario de datos
                        data.append({'Title': title, 'Price': price, 'Location': location, 'NumRoom': properties[0], 'NumBatrooms': properties[1], 'tamanoCostruccion': properties[2]})


                        #print(f"Numero: {cont} Title: {title}, Price: {price}, localizacion; {location}, NumRoom:{properties[0]}, NumBatrooms: {properties[1]}, tamanoCostruccion: {properties[2]}")

                        #print(f"Numero: {cont} Title: {title}, Price: {price}, localizacion: {location}")
                       
                    
                    pagination = soup.find('div', class_='pagination')
                    if pagination:
                        links = pagination.find_all('a', href=True)
                        for link in links:
                            absolute_url = link['href']
                            if absolute_url not in visited_links:
                                    pages_to_visit.append(absolute_url)
                            #pages_to_visit.append(absolute_url)
                    else:
                        print("pagination not found")

                    pages_visited += 1
                    visited_links.add(url)
                else:
                    print("code error in status", response.status_code)
                
            except Exception as e:
                print(f"Error crawling {url}: {e}")

    print(f"Finished crawling {pages_visited} pages.")
    # Convertir la lista de datos en un DataFrame de Pandas
    df = pd.DataFrame(data)
    # Guardar el DataFrame en un archivo CSV
    df.to_csv('C:/Users/isra/Desktop/mineria de datos/dataPrueba.csv', index=False, encoding = 'iso-8859-1')  # index=False para evitar que se añada una columna de índices
    #df.to_csv(data.csv, index=False, encoding = 'iso-8859-1')
# Example usage
seed_url = 'https://www.lamudi.com.mx/jalisco/casa/for-sale/'
max_pages = 85
crawl_web(seed_url, max_pages)

