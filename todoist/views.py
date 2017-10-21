# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings

from django.http import HttpResponse

from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from models import *
from django.views.generic import *
from django.urls import reverse_lazy

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from todoist.serializers import *


# Create your views here.
#def home(request):
#   return HttpResponse("hello world");
def render_lists(request):
    lists = ToDoList.objects.all()
    return render(request,"todo/lists.html",{"lists" : lists})

def render_items(request,id):
    list_id = int(id)
    list_name = ToDoList.objects.get(pk=list_id)
    #list_name = item.to_do_list_foreignKey.name
    items = ToDoItem.objects.filter(to_do_list_foreignKey_id = list_id)
    return render(request,"todo/items.html",{"items" : items , "name" : list_name})

def render_data(request):
    lists = ToDoList.objects.all()
    items = ToDoItem.objects.all()
    return render(request,"todo/data.html",{"items" : items , "lists" : lists})

class list_view(ListView):
    model = ToDoList
    context_object_name = 'lists'

class todo_details_view(DetailView):
    model = ToDoList
    slug_field = 'name'
    template_name = 'onlineapp/items.html'
    def get_context_data(self, **kwargs):
        context = super(todo_details_view,self).get_context_data(**kwargs)
        list_name = context['todolist']
        context['name'] = list_name
        context['items'] = ToDoItem.objects.filter(todolist__name = list_name)
        return context

from django.shortcuts import get_object_or_404

class CreateList(CreateView,RedirectView):
    model = ToDoList
    fields = ['name','CreationDate']
    success_url = reverse_lazy('create_item')
    pass

class CreateItem(CreateView):
    model = ToDoItem
    fields = ['description','completed','due_date','to_do_list_foreignKey']
    success_url = reverse_lazy('lists')
    pass

class UpdateList(UpdateView):
    model = ToDoList
    fields = ['name', 'CreationDate']
    success_url = reverse_lazy('lists')
    pass

class UpdateItem(UpdateView):
    model = ToDoItem
    fields = ['description', 'completed', 'due_date', 'to_do_list_foreignKey']
    success_url = reverse_lazy('lists')

class DeleteList(DeleteView):
    model = ToDoList
    success_url = reverse_lazy('lists')
    pass

@csrf_exempt
def list_serializer_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        list = ToDoList.objects.get(pk=pk)
    except ToDoList.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = TodoListSerializer(list)
        return JsonResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TodoListSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = TodoListSerializer(list, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        list.delete()
        return HttpResponse(status=204)

@csrf_exempt
def list_serializer(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = ToDoList.objects.filter(user_foreignKey = request.user.id)
        serializer = TodoListSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        name = request.POST.get("name")
        list = ToDoList(user_foreignKey=request.user.id, name = name, CreationDate= datetime.now())
        list.save()
        return HttpResponse("Done")
        # return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def item_serializer_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        item = ToDoItem.objects.get(pk=pk)
    except ToDoItem.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = TodoItemSerializer(item, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        item.delete()
        return HttpResponse(status=204)

@csrf_exempt
def list_id_item_serializer_detail(request):

    if request.method == 'POST':

        description = request.POST.get("description")
        completed = request.POST.get("completed")
        to_do_list_foreignKey = int(request.POST.get("to_do_list_foreignKey"))
        item = ToDoItem(to_do_list_foreignKey_id=to_do_list_foreignKey, description=description, completed=completed)
        item.save()
        return HttpResponse("Done")
        #return JsonResponse({'message': "Success"}, status=201)


@csrf_exempt
def list_id_item_serializer_detail1(request,pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        items = ToDoItem.objects.filter(to_do_list_foreignKey_id = pk)
        #id = request.POST.get("listId");
        #items  = ToDoItem.objects.filter(to_do_list_foreignKey_id = int(id))
    except items.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = TodoItemSerializer(items, many=True)
        return JsonResponse(serializer.data,safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TodoItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)



def logout_user(request):
    return render(request, 'new_todo/login_page.html', {})

def login_form(request):
    return render(request, 'new_todo/login_page.html', {})

@csrf_exempt
def get_auth_token(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        # the password verified for the user
        if user.is_active:
            token, created = Token.objects.get_or_create(user=user)
            request.session['auth'] = token.key
            login(request, user)
            return redirect('/todo/index/',method = "GET")
    else:
        return HttpResponse("incorrect credentials")

def index(request):
    return render(request, "new_todo/user_list1.html")

def create_account(request):

    username = request.POST.get('username')
    password = request.POST.get('password')
    console.log("hi");
    user = User.objects.create_user(username = username,password = password)

    user.save()
    return render("new_todo/login_page.html")