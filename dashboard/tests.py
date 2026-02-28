from django.test import TestCase, Client
from django.urls import reverse
from django.test.utils import override_settings
import pandas as pd
import os
from dashboard.models import TitanicPassenger


class TitanicPassengerModelTest(TestCase):
    def setUp(self):
        TitanicPassenger.objects.create(
            name="John Doe",
            sex="male",
            age=30,
            fare=50.0,
            survived=True,
            embarked="S",
            pclass=1
        )
        TitanicPassenger.objects.create(
            name="Jane Smith",
            sex="female",
            age=25,
            fare=30.0,
            survived=False,
            embarked="C",
            pclass=2
        )

    def test_passenger_creation(self):
        male = TitanicPassenger.objects.get(sex="male")
        female = TitanicPassenger.objects.get(sex="female")
        self.assertEqual(male.name, "John Doe")
        self.assertEqual(female.name, "Jane Smith")

    def test_passenger_str(self):
        passenger = TitanicPassenger.objects.get(sex="male")
        self.assertEqual(str(passenger), "John Doe")

    def test_total_count(self):
        self.assertEqual(TitanicPassenger.objects.count(), 2)
        self.assertEqual(TitanicPassenger.objects.filter(sex="male").count(), 1)
        self.assertEqual(TitanicPassenger.objects.filter(sex="female").count(), 1)

    def test_survived_count(self):
        self.assertEqual(TitanicPassenger.objects.filter(survived=True).count(), 1)
        self.assertEqual(TitanicPassenger.objects.filter(survived=False).count(), 1)

    def test_total_fare(self):
        total_fare = sum(TitanicPassenger.objects.values_list("fare", flat=True))
        self.assertEqual(total_fare, 80.0)


class DashboardViewTest(TestCase):
    def setUp(self):
        TitanicPassenger.objects.create(
            name="Test Passenger",
            sex="male",
            age=25,
            fare=100.0,
            survived=True,
            embarked="S",
            pclass=1
        )

    @override_settings(MEDIA_ROOT='test_media')
    def test_index_view_status_code(self):
        client = Client()
        response = client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    @override_settings(MEDIA_ROOT='test_media')
    def test_index_view_context_data(self):
        client = Client()
        response = client.get(reverse('index'))
        self.assertIn('total_passenger', response.context)
        self.assertIn('total_male', response.context)
        self.assertIn('total_female', response.context)
        self.assertIn('total_fare', response.context)
        self.assertIn('total_survived', response.context)
        self.assertIn('survived_rate', response.context)
        self.assertIn('classes', response.context)
        self.assertIn('count_by_class', response.context)
        self.assertIn('survived_by_class', response.context)
        self.assertIn('died_by_class', response.context)
        self.assertIn('top_10_fares', response.context)
        self.assertIn('ports', response.context)
        self.assertIn('embarked_by_class', response.context)

    @override_settings(MEDIA_ROOT='test_media')
    def test_index_view_kpi_values(self):
        client = Client()
        response = client.get(reverse('index'))
        
        self.assertEqual(response.context['total_passenger'], 1)
        self.assertEqual(response.context['total_male'], 1)
        self.assertEqual(response.context['total_female'], 0)
        self.assertEqual(response.context['total_fare'], "$ 0K")

    @override_settings(MEDIA_ROOT='test_media')
    def test_index_view_chart_data_structure(self):
        client = Client()
        response = client.get(reverse('index'))
        
        self.assertIsInstance(response.context['classes'], list)
        self.assertIsInstance(response.context['count_by_class'], list)
        self.assertIsInstance(response.context['survived_by_class'], list)
        self.assertIsInstance(response.context['died_by_class'], list)
        self.assertIsInstance(response.context['top_10_fares'], list)
        self.assertIsInstance(response.context['ports'], list)
        self.assertIsInstance(response.context['embarked_by_class'], list)


class CSVDataTest(TestCase):
    def test_csv_file_exists(self):
        csv_path = "static/data/titanic.csv"
        self.assertTrue(os.path.exists(csv_path))

    def test_csv_file_structure(self):
        df = pd.read_csv("static/data/titanic.csv")
        expected_columns = ['PassengerId', 'Survived', 'Pclass', 'Name', 'SAgeex', 'Unnamed: 5', 'SibSp', 'Parch', 'Ticket', 'Fare', 'Cabin', 'Embarked']
        for col in expected_columns:
            self.assertIn(col, df.columns)

    def test_csv_data_integrity(self):
        df = pd.read_csv("static/data/titanic.csv")
        self.assertGreater(len(df), 0)
        self.assertIn('Survived', df.columns)
        self.assertIn('Pclass', df.columns)
        self.assertIn('Fare', df.columns)


class URLTest(TestCase):
    def test_index_url_resolves(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_index_url_name(self):
        url = reverse('index')
        self.assertEqual(url, '/')
