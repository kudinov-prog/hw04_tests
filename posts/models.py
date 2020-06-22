from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Group(models.Model):

    title = models.CharField("Название", max_length=200)
    slug = models.SlugField("Путь", unique=True)
    description = models.TextField("Описание")

    def __str__(self):
        return self.title


class Post(models.Model):

    text = models.TextField("Текст публикации")
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name="Автор")
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, blank=True,
                              null=True, related_name="posts",
                              verbose_name="Сообщество")

    def __str__(self):
        return self.text

    class Meta:
        ordering = ["-pub_date"]
