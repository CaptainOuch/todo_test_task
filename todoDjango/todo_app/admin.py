from django.contrib import admin
from todo_app.models import TodoList, TodoItem

admin.site.register(TodoList)
admin.site.register(TodoItem)
