import json

from django.contrib.postgres.search import SearchVector
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet
from django.db.models.functions import Coalesce
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .models import Lek, SzczegolyRefundacji
from django.http import JsonResponse
from django.core import serializers
from rest_framework.renderers import JSONRenderer
from itertools import chain
import threading

from .serializers import LekSerializer

current_results = {
    'query': str,
    'query_result': QuerySet
}

offset = 100

start_index = 0

last_request: WSGIRequest

sort_request: WSGIRequest

is_sorted: bool


def update_offset():
    global offset, start_index
    offset += 100
    start_index += 100


def reset_offset():
    global offset, start_index
    offset = 100
    start_index = 0

def set_max_offset():
    global offset
    offset = 6000


def home(request):
    global last_request
    last_request = request
    print(request)
    context = {
        'query': '',
        'query_result': {}
    }
    return render(request, 'DrugSearch/leki.html', context)


def load_initial_data(request):
    global last_request, is_sorted
    is_sorted = False
    if request.path != '/get_more_results/':
        last_request = request
        reset_offset()
    print(request)
    print("load_initial_data")
    query = ""
    if request.method == 'GET':
        query_result = Lek.objects.all().order_by('pk')[start_index:offset]
        serialized_query = LekSerializer(query_result, many='True').data
        context = {  # create context for JSON response
            'query': query,
            'query_result': serialized_query
        }
        print("REURNED LOAD INITIAL DATA")
        return JsonResponse(context, safe=False)


def search_results(request):
    global last_request, is_sorted
    if request.path != '/get_more_results/':
        last_request = request
        reset_offset()
    else:
        request = last_request

    print("In search result")
    search_vec = SearchVector("nazwa_leku", "substancja_czynna", "postac", "dawka_leku", "zawartosc_opakowania",
                              "identyfikator_leku", "refundacje__zakres_wskazan",
                              "refundacje__zakres_wskazan_pozarejestracyjnych",
                              "refundacje__poziom_odplatnosci", "refundacje__wysokosc_doplaty")
    query = request.GET.get('query')
    print(query)
    if request.method == 'GET':
        query_result = Lek.objects.annotate(search=search_vec).\
                           filter(search__icontains=query).order_by('pk')[start_index:offset]  # filter the database
        serialized_query = LekSerializer(query_result, many='True').data
        print(serialized_query)
        context = {  # create context for JSON response
            'query': query,
            'query_result': serialized_query
        }
        return JsonResponse(context, safe=False)
    else:
        query_result = Lek.objects.all()
        serialized_query = LekSerializer(query_result, many='True').data
        context = {
            'query': query,
            'query_result': serialized_query
        }
        print(context)
        return render(request, 'DrugSearch/leki.html', context)


def sort_results(request):
    global last_request, sort_request, is_sorted, start_index
    reset_table = False
    if request.path == "/sort_results/":
        reset_offset()
        reset_table = True

    elif request.path == "/get_more_results/":
        reset_table = False
        request = last_request

    search_vec = SearchVector("nazwa_leku", "substancja_czynna", "postac", "dawka_leku", "zawartosc_opakowania",
                              "identyfikator_leku", "refundacje__zakres_wskazan",
                              "refundacje__zakres_wskazan_pozarejestracyjnych",
                              "refundacje__poziom_odplatnosci", "refundacje__wysokosc_doplaty")

    sort_by_key = request.GET.get("sort_by")
    sort_by_dir = request.GET.get("sort_direction")
    query = request.GET.get("query")
    last_request = request
    if request.method == 'GET':
        if query == "":
            if sort_by_dir == 'descending':
                sorted_results = Lek.objects.all().order_by('-'+sort_by_key, 'pk')[start_index:offset]
            else:
                sorted_results = Lek.objects.all().order_by(sort_by_key, 'pk')[start_index:offset]
        else:
            if sort_by_dir == 'descending':
                sorted_results = Lek.objects.annotate(search=search_vec).\
                                     filter(search__icontains=query).\
                                     order_by('-'+sort_by_key, 'pk')[start_index:offset]  # filter the database
            else:
                sorted_results = Lek.objects.annotate(search=search_vec).\
                                     filter(search__icontains=query).\
                                     order_by(sort_by_key, 'pk')[start_index:offset]  # filter the database

        serialized_query = LekSerializer(sorted_results, many='True').data
        context = {  # create context for JSON response
            'query': query,
            'query_result': serialized_query,
            'reset_table': reset_table
        }
        is_sorted = True
        return JsonResponse(context, safe=False)


def get_more_results(request):
    print(last_request)
    query = request.GET.get('load_all')
    if query:
        update_offset()
        set_max_offset()
        print("LOAD_ALL_ELEMENTS")
    else:
        update_offset()
    if last_request.path == "/load_initial_data/":
        print("get more after load initial data")
        return load_initial_data(request)
    elif last_request.path == "/sort_results/":
        print("get more after sort_results")
        return sort_results(request)
    elif last_request.path == "/search_results/":
        print("get more after search_results")
        return search_results(request)
    return JsonResponse({}, safe=False)


