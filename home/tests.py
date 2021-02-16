from django.test import TestCase, Client

# Create your tests here.
from .scrabber import Scrabber

class TestScrabber(TestCase):

    def setUp(self):
        self.urls = [
            'https://www.trendyol.com/trendyol-man/beyaz-erkek-basic-pamuklu-kisa-kollu-bisiklet-yaka-slim-fit-t-shirt-tmnss19bo0001-p-4032898',
            'https://www.defacto.com.tr/kapusonlu-slim-fit-kalin-mont-1577582',
            'https://www.suwen.com.tr/p/erkek-bambu-corap-siyah-sc1183012-2908?OM.zn=Category%20-%20Topviews-w24&OM.zpc=SC1183012',
        ]

        self.not_found_urls = [
            'http://google.com', 
            'https://www.trendyol.com/',
            'https://www.trendyol.com/trendyol-man/'
        ]

    def test_fake_urls(self):
        # Testing Fake urls
        self.assertEqual(Scrabber(False).prices[0], 'Not found.')
        self.assertEqual(Scrabber(0).prices[0], 'Not found.')
        self.assertEqual(Scrabber('testFakseUrl').prices[0], 'Not found.')
        self.assertEqual(Scrabber(['Test1', 'test2']).prices[0], 'Not found.')

    def test_success_urls(self):
        # urls that the script can parse price
        for url in self.urls:
            length = len( Scrabber(url).prices )
            self.assertGreaterEqual(length, 1 )
            self.assertLessEqual( length , 3 )

    def test_not_found(self):
        # in case weepage html changed or other incompatibale webpage.
        for url in self.not_found_urls:
            self.assertGreaterEqual( Scrabber(url).prices[0], 'Not found.' )

class HomeTest(TestCase):

    def test_get_home_page(self):
        """ testing home page found. """
        c = Client()
        res = c.get('/')
        self.assertEqual(res.status_code, 200)

class TestAPI(TestCase):

    def test_parse_price_success(self):
        c = Client()
        url = 'https://www.trendyol.com/trendyol-man/beyaz-erkek-basic-pamuklu-kisa-kollu-bisiklet-yaka-slim-fit-t-shirt-tmnss19bo0001-p-4032898'
        res = c.post('/api/get_price', data={"url":url})
        self.assertEqual(res.status_code, 200)
    
    def test_parse_price_error(self):
        c = Client()
        urls = ["google.com", False, 1, "test_url", ""]
        for url in urls: 
            res = c.post('/api/get_price', data={"url":url})
            self.assertEqual(res.status_code, 404)
            self.assertJSONEqual(str(res.content, encoding='utf8'), {"detail":["Not found."]})

    def test_parse_price_noUrl(self):
        c = Client()
        res = c.post('/api/get_price')
        self.assertEqual(res.status_code, 404)
        self.assertJSONEqual(str(res.content, encoding='utf8'), {"detail":["Not found."]})
    