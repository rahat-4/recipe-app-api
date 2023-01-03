"""Test tag model"""

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag
from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')

def tag_detail_url(tag_id):
    """"Return tag detail url"""

    return reverse('recipe:tag-detail', args=[tag_id])

def create_user(email='test@example.com',password='testpass123'):
    """Create and return new user"""

    return get_user_model().objects.create_user(email=email,password=password)

def create_tag(user, **params):
    """Create and return new tag"""

    defaults = {
        'name': 'Sample Tag'
    }

    defaults.update(params)
    tag = Tag.objects.create(user=user, **defaults)

    return tag


class PublicApiTests(TestCase):
    """Test for unauthenticated users"""

    def test_retrieve_tags(self):
        """Test retrieve all tags for unauthenticated user and get error"""

        self.client = APIClient()

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateApiTests(TestCase):
    """Test for authenticated users"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_retrieve_all_tags(self):
        """Test retrieve all tags for authenticated user."""

        create_tag(self.user, name='Vegan')
        create_tag(self.user, name='Dessert')

        tags = Tag.objects.all()

        res = self.client.get(TAGS_URL)
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_tag_limited_users(self):
        """Test retrieve tags for limited users"""

        other_user = create_user(email='new@example.com')
        tag = create_tag(user=self.user, name="Auth Tag")
        create_tag(user=other_user)

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)
        self.assertEqual(res.data[0]['id'], tag.id)

    def test_update_tag(self):
        """Test to update tag"""

        tag = create_tag(user=self.user)

        payload = {
            'name': 'New Tag-Update'
        }

        url = tag_detail_url(tag.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        tag.refresh_from_db()
        self.assertEqual(tag.name, payload['name'])

    def test_delete_tag(self):
        """Test delete tag"""

        tag = create_tag(user=self.user)

        url = tag_detail_url(tag.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        tags = Tag.objects.filter(user=self.user)
        self.assertFalse(tags.exists())



