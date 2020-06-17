from django.test import TestCase

# Create your tests here.


class TestStringMethods(TestCase):
    def test_length(self):
                self.assertEqual(len('yatube'), 6)

    def test_show_msg(self):
                # действительно ли первый аргумент — True?
                self.assertTrue(False, msg="Важная проверка на истинность")


class TestPostsMethods(TestCase):

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
