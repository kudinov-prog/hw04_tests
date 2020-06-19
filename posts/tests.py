from django.test import TestCase, Client
from .models import Post, Group, User


class TestPostsMethods(TestCase):

    def setUp(self):
        self.client = Client()

        self.test_text = 'old text'
        self.new_test_text = 'new text'
        self.test_message_id = '9999'

        self.new_user = User.objects.create_user(
          username='test_user', password='12345'
          )

        self.new_group = Group.objects.create(
          title='test_group', slug='test_group'
          )

        self.new_post = Post.objects.create(
          author=self.new_user,text=self.test_text,
          group=self.new_group,id=self.test_message_id
          )

        self.client.force_login(self.new_user)

    def test_create_profile_page(self):
        """ После регистрации пользователя создается его персональная 
            страница (profile)
        """
        response = self.client.get("/test_user/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["user"].username, self.new_user.username)


    def test_new_post(self):
        """Авторизованный пользователь может опубликовать пост (new)
        """
        data = {'text': self.test_text, "group": self.new_group}
        response = self.client.post("/new/", data=data, follow=True)
        self.assertEqual(response.status_code, 200)


    def test_redirect(self):
        """Неавторизованный посетитель не может опубликовать пост 
           (его редиректит на страницу входа)
        """
        self.client.logout()
        data = {'text': self.test_text, "group": self.new_group}
        response = self.client.post("/new/", data=data, follow=True)
        self.assertEqual(response.status_code, 200)


    def test_new_post_on_all_page(self):
        """После публикации поста новая запись появляется на главной странице 
           сайта (index), на персональной странице пользователя (profile), 
           и на отдельной странице поста (post)"""
        pass


    def test_user_edit(self):
        """Авторизованный пользователь может отредактировать свой пост и 
           его содержимое изменится на всех связанных страницах"""
        pass
