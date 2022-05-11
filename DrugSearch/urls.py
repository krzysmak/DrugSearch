from django.urls import path
from . import views

urlpatterns = [
    # path('results/', views.search_results_view, name='search_results'),
    path('', views.home, name='leki-home'),
    path('sort_results/', views.sort_results, name="sort_results"),
    path('search_results/', views.search_results, name="search_results")
]
