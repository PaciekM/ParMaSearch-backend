from django.urls import path


from search.views import SearchResults


urlpatterns = [
    path('search/', SearchResults.as_view(), name="search")
]
