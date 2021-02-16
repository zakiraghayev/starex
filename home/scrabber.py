import requests, re
from bs4 import BeautifulSoup


class Scrabber(object):
    """ Getting price of the products on the web page """
    
    def __init__(self, url):
        self.url = url
        self.requestHeaders = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"}
        self.currency = ' TL' # currency to find tag by 
        self.prices = [] # there could be 3 prices of one product (with discounts*)
        self.status = 0 # 200 OK
        self.hostname = "example.com"
        self.findTagbyCurrency() # automatically start to parse the product price

    def is_url(self):
        # validate the url inputed

        url = self.url
        if type(url) is str:
            regex = re.compile(
                r'^(?:http|ftp)s?://' # http:// or https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
                r'localhost|' #localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                r'(?::\d+)?' # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)
            
            if re.match(regex, url):
                return True
        return False
    
    def get_page(self):
        # check the url if valid get the web page ready to explore
        if not self.is_url():
            return False
        self.get_hostname()
        # Get web page ready to explore
        page = requests.get(self.url ,headers=self.requestHeaders)
        return BeautifulSoup(page.content,'html.parser')

    def get_hostname(self):
        # get domain of the web site to show
        # which website is requested
        arr = self.url.split('/')
        self.hostname = arr[2]

    def findTagbyCurrency(self):
        # Find all the ' TL' in the webpage
        # then find relevant TL price of the product

        soup = self.get_page()
        
        if not soup:
            self.prices = ["Not found."]
            self.status = 1 #404 not found
            return False

        # find all the ' TL' in the web 
        results = soup.find_all(string=re.compile(self.currency))

        for result in results:
            try:
                modified = result.parent.get_text().strip() # get rid of extra spaces
                # check if text has one space as "10 TL" does, if not error will follow
                pr, crr = modified.split(' ') 
                self.prices.append(modified)
            except:
                pass
        
        # | get rid of duplicates if any as they are not discount.
        self.prices = sorted(set(self.prices))

        # no price found in the website
        if len(self.prices) == 0:
            self.prices = ["Not found."]
            self.status = 1 #404 not found

    def print_prices(self):
        # print prices 
        print(*self.prices, sep = "\n")


