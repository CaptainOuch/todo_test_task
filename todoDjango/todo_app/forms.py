from django import forms

from todo_app.models import TodoItem


class TodoListSearchForm(forms.Form):
    search_query = forms.CharField(label='Search', max_length=100, required=False)


class TodoItemSearchForm(forms.Form):
    search_query = forms.CharField(label='Search', max_length=100, required=False)
    type = forms.ChoiceField(label='Type', choices=[('', '---')] + TodoItem.TYPE_CHOICES, required=False)
