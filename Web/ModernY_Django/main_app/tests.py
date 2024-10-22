from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import BlogPost

class MainAppTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.blog_post = BlogPost.objects.create(
            title='Test Blog Post',
            content='This is a test blog post content.',
            author=self.user
        )

    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app/home.html')

    def test_about_page(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app/about.html')

    def test_services_page(self):
        response = self.client.get(reverse('services'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app/services.html')

    def test_blog_list_page(self):
        response = self.client.get(reverse('blog_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app/blog_list.html')
        self.assertContains(response, 'Test Blog Post')

    def test_blog_detail_page(self):
        response = self.client.get(reverse('blog_detail', args=[self.blog_post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app/blog_detail.html')
        self.assertContains(response, 'Test Blog Post')
        self.assertContains(response, 'This is a test blog post content.')

    def test_contact_form_submission(self):
        response = self.client.post(reverse('contact'), {
            'name': 'Test User',
            'email': 'test@example.com',
            'subject': 'Test Subject',
            'message': 'This is a test message.'
        })
        self.assertEqual(response.status_code, 302)  # 假设成功提交后重定向
