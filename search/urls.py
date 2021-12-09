from django.urls import path


from search.views import ListUsers


urlpatterns = [
    path('search/', ListUsers.as_view(), name="search")
]
