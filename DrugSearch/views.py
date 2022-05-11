import json

from django.contrib.postgres.search import SearchVector
from django.db.models import QuerySet
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .models import Lek, SzczegolyRefundacji
from django.http import JsonResponse
from django.core import serializers
from rest_framework.renderers import JSONRenderer

from .serializers import LekSerializer

current_results = {}


def home(request):
        context = {
            'query': '',
            'query_result': Lek.objects.all()[:100]
        }
        global current_results
        current_results = context
        return render(request, 'DrugSearch/leki.html', context)


def search_results(request):
    print("In search result")
    search_vec = SearchVector("nazwa_leku", "substancja_czynna", "postac", "dawka_leku", "zawartosc_opakowania", "identyfikator_leku")
    print(request)
    data = request.GET.get('query')
    print("DATA " + data)
    query = data
    if request.method == 'GET':
        print("request method to GET")
        query_result = Lek.objects.annotate(search=search_vec).filter(search=query)
        # query_result = Lek.objects.all().values()
        serialized_query = LekSerializer(query_result, many='True').data
        context = {
            'query': query,
            'query_result': serialized_query
        }
        print(serialized_query)
        global current_results
        current_results = {
            'query': query,
            'query_result': query_result
        }
        print("returning")
        return JsonResponse(context, safe=False)
    else:
        print("request method to NIE GET")
        query_result = Lek.objects.all()
        context = {
            'query': query,
            'query_result': list(query_result.values())
        }
        print(context)
        return render(request, 'DrugSearch/leki.html', context)



def sort_results(request):
    sort_by_key = request.GET.get("sort_by")
    sort_by_dir = request.GET.get("sort_direction")
    if request.method == 'GET':
        global current_results
        if 'query_result' in current_results:
            sorted = current_results['query_result']
            if sort_by_dir == 'descending':
                sorted.order_by('-' + sort_by_key)
            else:
                sorted.order_by(sort_by_key)
            current_results['query_result'] = sorted
            context = {
                'query': current_results['query'],
                'query_result': list(sorted.values())
            }
            return JsonResponse(context, safe=False)
        else:
            context = {
                'query': '',
                'query_result': {}
            }
            return render(request, 'DrugSearch/leki.html', context)
