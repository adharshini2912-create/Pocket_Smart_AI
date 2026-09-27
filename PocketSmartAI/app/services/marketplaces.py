from urllib.parse import quote_plus
def search_url(platform,query):
    q=quote_plus(query); m={'Amazon':f'https://www.amazon.in/s?k={q}','Flipkart':f'https://www.flipkart.com/search?q={q}','IKEA':f'https://www.ikea.com/in/en/search/?q={q}','Swiggy':f'https://www.swiggy.com/search?query={q}','Zomato':f'https://www.zomato.com/search?query={q}','OYO':f'https://www.oyorooms.com/search?location={q}'}
    return m.get(platform,f'https://www.google.com/search?q={quote_plus(platform+" "+query)}')
