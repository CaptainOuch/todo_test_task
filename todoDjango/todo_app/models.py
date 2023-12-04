from django.db import models
from django.utils import timezone
from django.urls import reverse


def one_week_hence():
    return timezone.now() + timezone.timedelta(days=7)


class TodoList(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    title = models.CharField(max_length=58, unique=True)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    created_date = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('list', args=[self.id])

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_date']


class TodoItem(models.Model):
    TYPE_CHOICES = [
        ('Home', 'Home'),
        ('Work', 'Work'),
        ('Personal', 'Personal'),
        ('Shopping', 'Shopping'),
        ('Other', 'Other'),
    ]

    title = models.CharField(max_length=34)
    description = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, null=True, blank=True)
    due_date = models.DateTimeField(default=one_week_hence())
    todo_list = models.ForeignKey(TodoList, on_delete=models.CASCADE)
    file = models.FileField(upload_to='item_files/', null=True, blank=True)

    def get_absolute_url(self):
        return reverse(
            'item-update', args=[str(self.todo_list.id), str(self.id)]
        )

    def __str__(self):
        return f'{self.title} due: {self.due_date}'

    class Meta:
        ordering = ['created_date']
