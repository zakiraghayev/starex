from rest_framework import viewsets, response, status

from home.scrabber import Scrabber

class ScrabView(viewsets.ViewSet):
    """" API for getting price from the url """
    
    def parse_price(self, request):
        url = request.data.get('url', False)

        if not url:
            return response.Response({"detail":["Not found."]}, status=status.HTTP_404_NOT_FOUND)
        
        scrabber = Scrabber(url)

        res_status = [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
        data = {
            "detail":scrabber.prices,
            "other":scrabber.prices[1:],
            "real":scrabber.prices[0],
            "hostname":scrabber.hostname,
        }
        return response.Response(data, status=res_status[scrabber.status])