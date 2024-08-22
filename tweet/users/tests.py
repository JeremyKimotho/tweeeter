from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from user_profile.models import UserProfile

class UsersManagersTests(TestCase):
    
    def test_create_user(self):
        User = get_user_model()

        user = User.objects.create_user(
            email="normal@user.com", 
            password="foo", 
            user_name="mr_user", 
            date_of_birth=datetime(1999, 5, 26, 21, 12, 33, 675765, tzinfo=None))
        
        self.assertEqual(user.email, "normal@user.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            self.assertIsNotNone(user.user_name)
        except AttributeError:
            pass 
        # user cannot be created with no email
        with self.assertRaises(TypeError):
            User.objects.create_user()
        # user cannot be created with no password, user_name, date of birth
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        # user cannot be created with blank email
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="foo", user_name="mr_user2", date_of_birth=datetime(1999, 5, 26, 21, 12, 33, 675765, tzinfo=None))

        # Test user_profile created automatically
        user_profile = UserProfile.objects.filter(user_id = user.id)
        self.assertIsNotNone(user_profile)
         
    
    def test_create_superuser(self):
        User = get_user_model()

        admin_user = User.objects.create_superuser(
            email="super12@user.com", 
            password="foo", 
            user_name="mr_user", 
            date_of_birth=datetime(1999, 5, 26, 21, 12, 33, 675765, tzinfo=None))
        
        self.assertEqual(admin_user.email, "super12@user.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            self.assertIsNotNone(admin_user.user_name)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email = "", password="foo", user_name="mr_user", date_of_birth=datetime(1999, 5, 26, 21, 12, 33, 675765, tzinfo=None), is_superuser=False
            )

# Create your tests here.
