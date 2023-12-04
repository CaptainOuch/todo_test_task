from django.db.models import Q
from django.urls import reverse, reverse_lazy

from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .forms import TodoListSearchForm, TodoItemSearchForm
from .models import TodoList, TodoItem


class ListListView(ListView):
    model = TodoList
    template_name = 'todo_app/index.html'

    def get_queryset(self):
        queryset = TodoList.objects.all()
        search_query = self.request.GET.get('search_query')
        priority = self.request.GET.get('priority_filter')
        if search_query:
            queryset = queryset.filter(Q(title__icontains=search_query))
        if priority:
            queryset = queryset.filter(priority=priority)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        search_query = self.request.GET.get('search_query')
        form = TodoListSearchForm(initial={'search_query': search_query})
        context['form'] = form

        priority_filter = self.request.GET.get('priority_filter')
        context['priority_choices'] = TodoList.PRIORITY_CHOICES
        context['selected_priority'] = priority_filter
        return context


class ItemListView(ListView):
    model = TodoItem
    template_name = 'todo_app/todo_list.html'

    def get_queryset(self):
        queryset = TodoItem.objects.filter(todo_list_id=self.kwargs["list_id"])

        search_query = self.request.GET.get('search_query')
        if search_query:
            queryset = queryset.filter(Q(title__icontains=search_query))

        type_filter = self.request.GET.get('type')
        if type_filter:
            queryset = queryset.filter(type=type_filter)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        todo_list = TodoList.objects.get(id=self.kwargs["list_id"])
        context["todo_list"] = todo_list
        context['form'] = TodoItemSearchForm(initial={
            'search_query': self.request.GET.get('search_query'),
            'type': self.request.GET.get('type'),
        })
        context['description'] = todo_list.description
        return context


class ListCreate(CreateView):
    model = TodoList
    fields = ['title', 'description', 'priority']

    def get_context_data(self, **kwargs):
        context = super(ListCreate, self).get_context_data()
        context['title'] = 'Create new list'
        return context


class ItemCreate(CreateView):
    model = TodoItem
    fields = [
        'todo_list',
        'title',
        'description',
        'type',
        'due_date',
    ]

    def get_initial(self):
        initial_data = super(ItemCreate, self).get_initial()
        todo_list = TodoList.objects.get(id=self.kwargs['list_id'])
        initial_data['todo_list'] = todo_list
        return initial_data

    def get_context_data(self):
        context = super(ItemCreate, self).get_context_data()
        todo_list = TodoList.objects.get(id=self.kwargs['list_id'])
        context['todo_list'] = todo_list
        context['title'] = 'Create a new item'
        return context

    def get_success_url(self):
        return reverse('list', args=[self.object.todo_list_id])


class ItemUpdate(UpdateView):
    model = TodoItem
    fields = [
        'todo_list',
        'title',
        'description',
        'type',
        'due_date',
        'file',
    ]

    def get_context_data(self):
        context = super(ItemUpdate, self).get_context_data()
        context['todo_list'] = self.object.todo_list
        context['title'] = 'Edit item'
        return context

    def get_success_url(self):
        return reverse('list', args=[self.object.todo_list_id])


class ListDelete(DeleteView):
    model = TodoList

    def get_success_url(self):
        return reverse_lazy('index')


class ItemDelete(DeleteView):
    model = TodoItem

    def get_success_url(self):
        return reverse_lazy('list', args=[self.object.todo_list_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todo_list'] = self.object.todo_list
        return context
