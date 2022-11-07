import requests
from bs4 import BeautifulSoup
import pandas

homepage = 'https://www.alza.cz/'
url = 'https://www.alza.cz/EN/wireless-gaming-mice/18865199.htm'
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',

}
request = requests.get(url, headers=header).content
b = BeautifulSoup(request, 'lxml')
results_amount = int(b.find('div', class_='cpager__wrapper').text.split()[0])# getting amount of product
pages = round(results_amount / 24) # getting amount of pages
product_list = []
product_dict = {}
for page in range(1, pages + 1):
    modified_page_link = f"https://www.alza.cz/EN/wireless-gaming-mice/18865199-p{page}.htm"
    request = requests.get(modified_page_link, headers=header).content
    soup = BeautifulSoup(request, 'lxml')
    product_box = (soup.find_all('div', class_='browsingitem')) # product cards
    # print(links)
    for i in product_box: # going on each product page and taking all required info
        mouse_link = i.find('div', class_='fb').find('a', href=True)
        mouse_page = requests.get('https://www.alza.cz/' + mouse_link['href'], headers=header).content
        mouse_page_soup = BeautifulSoup(mouse_page, 'lxml')
        mouse_name = mouse_page_soup.find('div', class_='title-share').text.strip()
        print(f'Adding {mouse_name}')
        availability = mouse_page_soup.find("span", class_='avlVal').text.strip()
        price =''.join([i for i in mouse_page_soup.find("span", 'price-box__price-text').text.strip() if i.isdigit()])
        # print(price)
        discount = mouse_page_soup.find('span', 'price-box__header-text')
        # print(discount.text)
        if not discount or 'Discounted' not in discount.text:
            discount = 'No discount'
        else:
            discount = discount.text
        if not price.isdigit():
            price = 'Price has not been set'
        product_list.append([mouse_name, int(price) if price.isdigit() else price, availability, discount,f"https://www.alza.cz/{mouse_link['href']}"])

dataframe = pandas.DataFrame(product_list)
dataframe.columns = ['Name', 'Price', 'Availability', 'Discount','Link to store'] # setting column names
dataframe.to_csv('mouse_list.csv', header=['Name', 'Price', 'Availability', 'Discount','Link to store']) #creating csv file
# print(*product_list, sep='\n')
# print(dataframe.columns)