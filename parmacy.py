from bs4 import BeautifulSoup
import requests
import os
import pandas as pd
import json

def imageSave(imageUrl):
    page = requests.get(imageUrl['src'])
    f_name = os.path.split(imageUrl['src'])[-1]
    with open(f'images2/{f_name}', 'wb') as f:
        f.write(page.content)
    return f'images2/{f_name}'




products_links = []
for i in range(501, 1098):
    baseurl = f'https://www.epharma.com.bd/products?type=1&page={i}'
    page = requests.get(baseurl)
    soup = BeautifulSoup(page.content, 'html.parser')
    product_list = soup.find_all('ul', 'li', class_='products-list')
    #print(product_list)
    for item in product_list:
        #data = item.find_all('a', href=True)
        #print(data)
        # #print(item.find_all('a')
        for link in item.find_all('a', href=True, class_='product-image'):
            products_links.append(link['href'])
            #print(link['href'])
            #print(link['title'])

print('Links done')
products = []
count = 1
for link in products_links:
    #testlink = requests.get('https://www.epharma.com.bd/product/5163')
    try:

        testlink = requests.get(link)
        soup = BeautifulSoup(testlink.content, 'html.parser')
        name = soup.find('h1', class_='product-name').get_text().strip().replace("\n", "")
        description = soup.find('p', class_='availability').get_text().strip().replace("\n", "")
        price = soup.find('span', class_='product-price').get_text().strip().replace("\n", "")
        price_value = price[1:].split('(')[0].strip()
        imageDiv = soup.find('div', class_='product-img-wrapper')
        imageUrl = imageDiv.find('img')
        image = imageSave(imageUrl)
        product = {
            'name': name,
            'description': description,
            'price': price_value,
            'image': image
        }

        for item in soup.find_all('p'):
            value = item.get_text().strip().replace("\n", "")
            #print(value)
            if value[:11] == 'Categories:':
                product['category'] = value[11:]
            elif value[:8] == 'Generic:':
                product['generic'] = value[8:]
            elif value[:6] == 'Brand:':
                product['brand'] = value[6:]
            elif value[:5] == 'Type:':
                product['type_me'] = value[5:]

        products.append(product)
        print(f'Product added {count}')
        count = count+1
    except:
        pass




#print(product)

#
# df = pd.DataFrame(products)
# print(df.head(10))
# df.to_json('/home/sorwar/Documents/Python/scraping/products.json')

# Save local products
print(len(products))
with open('data2.json', 'w', encoding='utf-8') as f:
    json.dump(products, f, ensure_ascii=False, indent=4)
print('Done')


