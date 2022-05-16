from django.urls import path
from . import views

urlpatterns = [
    # path('results/', views.search_results_view, name='search_results'),
    path('', views.home, name='leki-home'),
    path('sort_results/', views.sort_results, name="sort_results"),
    path('search_results/', views.search_results, name="search_results"),
    path('load_initial_data/', views.load_initial_data, name="load_initial_data"),
    path('get_more_results/', views.get_more_results, name="get_more_results"),
]
