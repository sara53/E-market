from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import models
from myapp.models import Products
from myapp.models import Comments
from myapp.polarity_detector import detect_polarity
import json


@csrf_exempt
def mainView(request):
   return render(request, "index.html", {})


@csrf_exempt
def productView(request):
    # TODO handle product GET Request
    request.session['pid'] = int(request.GET['pid'])
    return render(request, "product.html", {})



@csrf_exempt
def compareView(request):
    # TODO handle compare GET Request
    compare_count = int(request.GET['count'])
    compare_ids_list = []
    for i in range(compare_count):
        compare_ids_list.append(int(request.GET['pid' + str(i+1)]))
    print('COUNT = ', compare_count)
    print('IDS LIST: ', compare_ids_list)
    request.session['compare_ids_list'] = compare_ids_list
    return render(request, "compare.html", {})


@csrf_exempt
def getCategories(request):
    gatcategories = Products.getCategories()
    return HttpResponse(json.dumps(gatcategories))


@csrf_exempt
def getBrands(request):
    # TODO handle get_brands POST Request
    gatbrands = Products.getBrands()
    return HttpResponse(json.dumps(gatbrands))


@csrf_exempt
def viewAllProducts(request):
    # TODO handle view_all_products POST Request
    name = request.POST['name']
    if name == '****':
        name = ''
    priceMin = int(request.POST['price_min'])
    priceMax = int(request.POST['price_max'])
    categoriesList = []
    categoriesListCount = int(request.POST['num_of_categories'])
    for i in range(categoriesListCount):
        categoriesList.append(request.POST['category' + str(i+1)])
    brandsList = []
    brandsListCount = int(request.POST['num_of_brands'])
    for i in range(brandsListCount):
        brandsList.append(request.POST['brand' + str(i + 1)])
    print(name, priceMin, priceMax, categoriesList, brandsList)
    allProducts = Products.getAllProducts(name, priceMin, priceMax, categoriesList, brandsList)
    return HttpResponse(json.dumps(allProducts))


@csrf_exempt
def view_product(request):
    # TODO handle view_all_products POST Request
    pid = request.session['pid']
    res = Products.getProduct(pid)
    print('PID NOW = ', pid)
    return HttpResponse(json.dumps(res))



@csrf_exempt
def view_comments(request):
    # TODO handle view_all_comments POST Request
    pid = request.session['pid']
    comment = Comments.viewComments(pid)
    return HttpResponse(json.dumps(comment))


@csrf_exempt
def add_comment(request):
    # TODO handle add_comments POST Request
    name = request.POST['name']
    comment = request.POST['comment']
    pid = request.session['pid']
    Comments.addComment(pid, name, comment)
    polarity = detect_polarity(comment, check_neutral=True, show_details=True)
    pos_percentage = Products.updateVotes(pid, polarity)
    return HttpResponse(json.dumps(pos_percentage))

@csrf_exempt
def compare_products(request):
    # TODO handle compare_comments POST Request
    pidslist = request.session['compare_ids_list']
    compare = Products.compareProducts(pidslist)
    return HttpResponse(json.dumps(compare))
