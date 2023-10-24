from django.test import TestCase

# Create your tests here.


class TestHome(TestCase):
    def setUp(self):
        self.response = self.client.get('/perfil/home/')

    def test_get_homne(self):
        """GET / must return status code 200"""
        self.assertEqual(self.response.status_code, 200)

    def test_template_used_in_home(self):
        """Must return a template home.html"""
        self.assertTemplateUsed(self.response, 'home.html')


class TestGerenciar(TestCase):
    def setUp(self):
        self.response = self.client.get('/perfil/gerenciar/')

    def test_get_gerenciar(self):
        """GET / must return status code 200"""
        self.assertEqual(self.response.status_code, 200)

    def test_template_used_in_gerenciar(self):
        """Must return a template gerenciar.html"""
        self.assertTemplateUsed(self.response, 'gerenciar.html')


class TestDashboard(TestCase):
    def setUp(self):
        self.response = self.client.get('/perfil/dashboard/')

    def test_get_dashboard(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template_used_in_dashboard(self):
        self.assertTemplateUsed(self.response, 'dashboard.html')
