from django.test import TestCase
from .models import Post, Group, User


class TestPostsMethods(TestCase):
    """
    1.После регистрации пользователя создается его персональная 
      страница (profile)
    2.Авторизованный пользователь может опубликовать пост (new)
    3.Неавторизованный посетитель не может опубликовать пост 
      (его редиректит на страницу входа)
    4.После публикации поста новая запись появляется на главной странице 
      сайта (index), на персональной странице пользователя (profile), 
      и на отдельной странице поста (post)
    5.Авторизованный пользователь может отредактировать свой пост и 
      его содержимое изменится на всех связанных страницах

    """

    def setUp(self):
        self.test_text = 'old text'
        self.new_test_text = 'new text'
        self.test_message_id = '9999'

        self.client = client()

        self.new_user = User.objects.create_user(username='test_user', password='12345')

        self.new_group = Group.objects.create(title='test_group', slug='test_group')

        self.new_post = Post.objects.create(author=self.new_user,
                                            text=self.test_text = 'old text',
                                            group=self.new_group,
                                            id=self.test_message_id = '9999')

    def test_profile_reg(self):
        pass

    def test_new_post(self):
        pass

    def test_redirect(self):
        pass

    def test_new_post_on_all_page(self):
        pass

    def test_user_edit(self):
        pass
