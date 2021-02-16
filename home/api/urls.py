from django.urls import path
from .views import ScrabView

urlpatterns =[
    path("get_price", ScrabView.as_view({"post":"parse_price"}) ),
]