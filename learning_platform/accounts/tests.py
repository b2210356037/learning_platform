# Create your tests here.
from django.test import TestCase
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm

User = get_user_model()

class RegisterViewTests(TestCase):
    def setUp(self):
        self.url = reverse('register')  # URL adını kontrol edin

    def test_register_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')  # Şablonun kullanıldığını kontrol et
        self.assertIsInstance(response.context['form'], CustomUserCreationForm)  # Form nesnesinin doğru türde olduğunu kontrol et

    def register_view_post_valid_data(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'name': 'Test',
            'surname': 'User',
            'password1': 'Testpassword123',
            'password2': 'Testpassword123',  
            'user_type': 1,
        }
        response = self.client.post(self.url, form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('accounts/course_list.html'))  # Başarıyla course_list'e yönlendirme
        self.assertTrue(User.objects.filter(username='testuser').exists())  # Kullanıcının oluşturulduğunu kontrol et

    def register_view_post_invalid_data(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'name': 'Test',
            'surname': 'User',
            'password1': 'Testpassword123',
            'password2': 'DifferentPassword123',  
            'user_type': 1,
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')  # Hata varsa aynı şablonun kullanıldığını kontrol et
        form = response.context['form']
        self.assertFalse(form.is_valid())  # Formun geçersiz olduğunu kontrol et
        self.assertFormError(response, 'form', 'password2', 'The two password fields must match.')  # Hata mesajını kontrol et


