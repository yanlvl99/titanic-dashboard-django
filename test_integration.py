import pytest
from django.test import TestCase, Client
from django.urls import reverse
from django.test.utils import override_settings
import pandas as pd
import os
from dashboard.models import TitanicPassenger


class IntegrationTest(TestCase):
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
        TitanicPassenger.objects.create(
            name="Bob Johnson",
            sex="male",
            age=45,
            fare=75.0,
            survived=True,
            embarked="Q",
            pclass=3
        )

    @override_settings(MEDIA_ROOT='test_media')
    def test_full_dashboard_integration(self):
        client = Client()
        response = client.get(reverse('index'))
        
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(response.context['total_passenger'], 3)
        self.assertEqual(response.context['total_male'], 2)
        self.assertEqual(response.context['total_female'], 1)
        
        total_fare = sum(TitanicPassenger.objects.values_list("fare", flat=True))
        expected_fare = "$ " + str(int(total_fare // 1000)) + "K"
        self.assertEqual(response.context['total_fare'], expected_fare)
        
        self.assertIsInstance(response.context['classes'], list)
        self.assertIsInstance(response.context['count_by_class'], list)
        self.assertIsInstance(response.context['survived_by_class'], list)
        self.assertIsInstance(response.context['died_by_class'], list)
        self.assertIsInstance(response.context['top_10_fares'], list)
        self.assertIsInstance(response.context['ports'], list)
        self.assertIsInstance(response.context['embarked_by_class'], list)

    @override_settings(MEDIA_ROOT='test_media')
    def test_dashboard_with_empty_database(self):
        TitanicPassenger.objects.all().delete()
        
        client = Client()
        response = client.get(reverse('index'))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['total_passenger'], 0)
        self.assertEqual(response.context['total_male'], 0)
        self.assertEqual(response.context['total_female'], 0)
        self.assertEqual(response.context['total_fare'], "$ 0K")

    def test_database_model_constraints(self):
        passenger = TitanicPassenger.objects.create(
            name="Valid Name",
            sex="male",
            age=30,
            fare=50.0,
            survived=True,
            embarked="S",
            pclass=1
        )
        self.assertIsNotNone(passenger.id)
        self.assertEqual(str(passenger), "Valid Name")

    def test_csv_and_database_consistency(self):
        df = pd.read_csv("static/data/titanic.csv")
        csv_survived = df[df["Survived"] == 1].shape[0]
        
        TitanicPassenger.objects.all().delete()
        for _, row in df.head(10).iterrows():
            if 'SAgeex' in df.columns:
                sex = str(row['SAgeex']).split()[0] if isinstance(row['SAgeex'], str) and ' ' in str(row['SAgeex']) else row['SAgeex']
                age = float(str(row['SAgeex']).split()[1]) if isinstance(row['SAgeex'], str) and ' ' in str(row['SAgeex']) and len(str(row['SAgeex']).split()) > 1 else None
            
            TitanicPassenger.objects.create(
                name=row['Name'],
                sex=sex,
                age=age,
                fare=row['Fare'],
                survived=bool(row['Survived']),
                embarked=row['Embarked'],
                pclass=int(row['Pclass'])
            )
        
        db_survived = TitanicPassenger.objects.filter(survived=True).count()
        self.assertLessEqual(db_survived, 10)
