from django.contrib.auth.models import User
from django.db import models


class Chat(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    clients = models.ManyToManyField(User, blank=True, verbose_name='Пользователи')

    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    update_date = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'
        ordering = ['-update_date']

    def __str__(self):
        return f'{self.title}'


class Message(models.Model):
    text = models.TextField(verbose_name='Текст')
    chat = models.ForeignKey('chat.Chat', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Отправитель')

    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    update_date = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['-creation_date']

    def __str__(self):
        return f'{self.text}'
