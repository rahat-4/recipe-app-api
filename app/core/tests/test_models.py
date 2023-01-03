from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal

from core import models
from unittest.mock import patch

def create_user(email='test@example.com',password='testpass123'):
    """Create and return new user"""

    return get_user_model().objects.create_user(email, password)

class ModelTests(TestCase):
    """Test models"""

    def test_create_user_with_email_successful(self):
        """Test creating user with an email is successful"""
        email = "test@example.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_user_email_normailized(self):
        """Test email is normalized for new users."""

        sample_email = [
            ['test1@example.Com', 'test1@example.com'],
            ['Test2@examplE.CoM', 'Test2@example.com'],
            ['TEST3@EXAMPLE.Com', 'TEST3@example.com'],
            ['tESt4@EXAMPLE.COM', 'tESt4@example.com'],
        ]

        for email, expected in sample_email:
            user = get_user_model().objects.create_user(email, 'sample123pass')

            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raise_error(self):
        """Test creating new user without email raise error."""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123pass')

    def test_create_superuser(self):
        """Test creating superuser"""

        user = get_user_model().objects.create_superuser(
            'test10@example.com',
            'test123pass'
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_recipe_success(self):
        """Test create receipe successfully."""

        user = create_user()

        recipe = models.Recipe.objects.create(
            user=user,
            title="Sample title",
            time_minutes=5,
            price=Decimal('5.50'),
            description="Sample Description",
        )

        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        """Test tag create successfully."""

        user = create_user()

        tag = models.Tag.objects.create(
            user=user,
            name='Sample Tag'
        )

        self.assertEqual(str(tag), tag.name)

    @patch('core.models.uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test generating image path."""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'example.jpg')

        self.assertEqual(file_path, f'uploads/recipe/{uuid}.jpg')