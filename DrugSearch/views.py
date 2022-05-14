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
    global last_request
    last_request = request
    print(request)
    print("load_initial_data")
    query = ""
    if request.method == 'GET':
        global start_index
        query_result = Lek.objects.all()[:offset]
        start_index += offset
        serialized_query = LekSerializer(query_result, many='True').data
        context = {  # create context for JSON response
            'query': query,
            'query_result': serialized_query
        }
        global current_results  # update current results
        current_results = {
            'query': query,
            'query_result': query_result
        }
        return JsonResponse(context, safe=False)


def search_results(request):
    global last_request
    last_request = request
    print("In search result")
    search_vec = SearchVector("nazwa_leku", "substancja_czynna", "postac", "dawka_leku", "zawartosc_opakowania",
                              "identyfikator_leku", "refundacje__zakres_wskazan",
                              "refundacje__zakres_wskazan_pozarejestracyjnych",
                              "refundacje__poziom_odplatnosci", "refundacje__wysokosc_doplaty")
    query = request.GET.get('query')
    if request.method == 'GET':
        query_result = Lek.objects.annotate(search=search_vec).filter(search__icontains=query)[:offset]  # filter the database
        serialized_query = LekSerializer(query_result, many='True').data
        print(serialized_query)
        context = {  # create context for JSON response
            'query': query,
            'query_result': serialized_query
        }
        global current_results  # update current results
        current_results = {
            'query': query,
            'query_result': query_result
        }
        return JsonResponse(context, safe=False)
    else:
        query_result = Lek.objects.all()
        serialized_query = LekSerializer(query_result, many='True').data
        context = {
            'query': query,
            'query_result': serialized_query
        }
        current_results = {
            'query': query,
            'query_result': query_result
        }
        print(context)
        return render(request, 'DrugSearch/leki.html', context)


def sort_results(request):
    global last_request
    last_request = request
    search_vec = SearchVector("nazwa_leku", "substancja_czynna", "postac", "dawka_leku", "zawartosc_opakowania",
                              "identyfikator_leku", "refundacje__zakres_wskazan",
                              "refundacje__zakres_wskazan_pozarejestracyjnych",
                              "refundacje__poziom_odplatnosci", "refundacje__wysokosc_doplaty")
    print("sorting")
    print(request)
    sort_by_key = request.GET.get("sort_by")
    sort_by_dir = request.GET.get("sort_direction")
    query = request.GET.get("query")
    if request.method == 'GET':
        if query == "":
            if sort_by_dir == 'descending':
                sorted_results = Lek.objects.all().order_by('-'+sort_by_key)[:offset]
            else:
                sorted_results = Lek.objects.all().order_by(sort_by_key)[:offset]
        else:
            if sort_by_dir == 'descending':
                sorted_results = Lek.objects.annotate(search=search_vec).filter(search__icontains=query).order_by('-'+sort_by_key)[:offset]  # filter the database
            else:
                sorted_results = Lek.objects.annotate(search=search_vec).filter(search__icontains=query).order_by(sort_by_key)[:offset]  # filter the database

        serialized_query = LekSerializer(sorted_results, many='True').data
        context = {  # create context for JSON response
            'query': query,
            'query_result': serialized_query
        }
        return JsonResponse(context, safe=False)


def get_more_results(request):
    query = request.GET.get('query')
    global start_index
    result = Lek.objects.all()[start_index:offset]
    start_index += offset
    serialized_query = LekSerializer(result, many='True').data
    context = {  # create context for JSON response
        'query': query,
        'query_result': serialized_query
    }
    global current_results  # update current results
    current_results = {
        'query': query,
        'query_result': result
    }
    return JsonResponse(context, safe=False)
