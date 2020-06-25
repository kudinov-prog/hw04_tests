from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.test import TestCase, Client
from .models import Post, Group, User


class TestPostsMethods(TestCase):

    def setUp(self):
        self.client = Client()

        self.test_text = 'old text'
        self.new_test_text = 'new text'
        self.test_message_id = '1111'

        self.new_user = User.objects.create_user(
          username='test_user', password='12345'
          )

        self.test_group = Group.objects.create(
          title='test_group', slug='test_group'
          )
        self.new_test_group = Group.objects.create(
          title='new_test_group', slug='new_test_group'
          )

        self.new_post = Post.objects.create(
          author=self.new_user, text=self.test_text,
          group=self.test_group,id=self.test_message_id
          )

        self.client.force_login(self.new_user)

    def test_create_profile_page(self):
        """ После регистрации пользователя создается его персональная 
            страница (profile)
        """

        response = self.client.get("/test_user/")
        self.assertEqual(response.context["user"].username,
                         self.new_user.username)

    def test_new_post(self):
        """ Авторизованный пользователь может опубликовать пост (new)
        """

        data = {'text': self.test_text, "group": self.test_group}
        response = self.client.post(reverse("new_post"),
                                    data=data, follow=True)

        post = Post.objects.get(id=self.test_message_id)
        check_list = (post.text, post.group, post.author)

        for item in check_list:
            self.assertContains(response, item)
        
        self.assertEqual(response.status_code, 200)
        
    def test_unauthorized_user_post(self):
        """ Неавторизованный посетитель не может опубликовать пост 
            (его редиректит на страницу входа)
        """

        self.client.logout()

        data = {'text': self.test_text, "group": self.test_group}
        response = self.client.post(reverse("new_post"),
                                    data=data, follow=True)
        
        posts_count = Post.objects.all().count()

        self.assertEqual(posts_count, 1)
        self.assertRedirects(response, '/auth/login/?next=/new/')

    def check_post(self, url, text, group, author):
        
            response = self.client.get(url, follow=True)
            paginator = response.context.get('paginator')
            
            if paginator is not None:
                post = response.context['page'][0]
            else:
                post = response.context['post']
                
            self.assertEqual(post.text, text)
            self.assertEqual(post.group, group)
            self.assertEqual(post.author, author)

    def test_new_post_on_all_page(self):
        """ После публикации поста новая запись появляется на главной странице 
            сайта (index), на персональной странице пользователя (profile), 
            и на отдельной странице поста (post)
        """

        urls = (reverse('index'),
                reverse('profile',
                        kwargs={'username': self.new_user.username}),
                reverse('post',
                        kwargs={'username': self.new_user.username,
                                'post_id': self.test_message_id}))

        for url in urls:
            self.check_post(url, self.new_post.text,
                                 self.new_post.group,
                                 self.new_post.author)

    def test_user_edit(self):
        """ Авторизованный пользователь может отредактировать свой пост и 
            его содержимое изменится на всех связанных страницах
        """

        self.client.post(reverse('post_edit',
            kwargs={'username': self.new_user.username,
                    'post_id': self.new_post.id}),
            data={'text': self.new_test_text, 'group': self.new_test_group},
            follow=True)

        urls = (reverse('index'),
                reverse('group_posts',
                        kwargs={'slug': self.test_group.slug}),
                reverse('profile',
                        kwargs={'username': self.new_user.username}),
                reverse('post',
                        kwargs={'username': self.new_user.username,
                        'post_id': self.new_post.id}))
        
        for url in urls:
            self.check_post(url, self.new_post.text,
                                 self.new_post.group,
                                 self.new_post.author)
