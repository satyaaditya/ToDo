from rest_framework import serializers
from todoist.models import *

class TodoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDoList
        fields = ('name', 'CreationDate','user_foreignKey','id')

class TodoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDoItem
        fields = ('description','completed','due_date','to_do_list_foreignKey','id')

