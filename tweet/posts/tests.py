import datetime  

from django.test import TestCase
from django.test.client import Client
from django.utils import timezone
from django.urls import reverse 

from posts.models import Comment
from posts.models import Post
from posts.models import Quote    
from users.models import CustomUser
from user_profile.models import UserProfile

class PostCreationDeletionTests(TestCase):
    def login(self):
        self.email = 'test@test.com'
        self.username = 'test1'
        self.password = 'password1'

        user = CustomUser.objects.create_user(email=self.email, user_name=self.username, password=self.password,date_of_birth=datetime.datetime(1999, 5, 26, 21, 12, 33, 675765, tzinfo=None))
        user.save()

        client = Client()
        client.login(email=self.email, password=self.password)
        
        user_profile = UserProfile.objects.get(user=user)
        return user_profile, client
    

    def create_test_post(self):
        test_user = CustomUser.objects.create_user(email='test1@test.com', user_name='test2', password='password2', date_of_birth=datetime.datetime(1999, 5, 26, 21, 12, 33, 675765, tzinfo=None))
        test_user.save()

        profile = UserProfile.objects.get(user=test_user)

        post = Post.objects.create(poster=profile, body='test body, this can be any text just make sure its nothing important')
        post.save()
        return post, profile
    

    def create_test_quote(self):
        test_user = CustomUser.objects.create_user(email='test3@test.com', user_name='test4', password='password3', date_of_birth=datetime.datetime(1999, 5, 26, 21, 12, 33, 675765, tzinfo=None))
        test_user.save()

        profile = UserProfile.objects.get(user=test_user)

        post = Post.objects.create(poster=profile, body='test body 2, this can be any text just make sure its nothing important')
        post.save()

        quote = Quote.objects.create(poster=profile, body='test body 2, this can be any text just make sure its nothing important', quote_post=post)
        quote.save()
        
        return quote

    def create_test_comment(self):
        test_user = CustomUser.objects.create_user(email='test4@test.com', user_name='test5', password='password4', date_of_birth=datetime.datetime(1999, 5, 26, 21, 12, 33, 675765, tzinfo=None))
        test_user.save()

        profile = UserProfile.objects.get(user=test_user)

        post = Post.objects.create(poster=profile, body='test body 2, this can be any text just make sure its nothing important')
        post.save()

        comment = Comment.objects.create(poster=profile, body='test body 2, this can be any text just make sure its nothing important', reply_post=post)
        comment.save()
        
        return comment   
    

    def test_create_post_as_normal(self):
        test_user, client = self.login()

        url = reverse('posts:create_post')
        response = client.post(url, data={'poster':test_user, 'body':'test body, this can be any text just make sure its nothing important'}, follow=True)

        # Check the response is ok and db reflects change caused by 'post'
        self.assertEqual(response.status_code, 200)

        # Check the 'post' exists
        try:
            Post.objects.get(poster_id=test_user.id)
        except Post.DoesNotExist:
            print("Post record does not exist")
            self.assertTrue(False)

        client.logout()


    def test_create_post_user_not_authenticated(self):
        test_user, client = self.login()
        
        client.logout()

        url = reverse('posts:create_post')
        response = client.post(url, data={'poster':test_user, 'body':'test body, this can be any text just make sure its nothing important'}, follow=True)

        # Correctly redirects unauthenticated users to login page
        self.assertNotEqual(response.status_code, 200)


    def test_delete_post_normal_use(self):
        test_user, client = self.login()

        url = reverse('posts:create_post')
        response = client.post(url, data={'poster':test_user, 'body':'test body, this can be any text just make sure its nothing important'}, follow=True)

        # Check the response is ok and db reflects change caused by 'post'
        self.assertEqual(response.status_code, 200)

        # Check the 'post' exists
        try:
            test_post = Post.objects.get(poster_id=test_user.id)
        except Post.DoesNotExist:
            print("Post record does not exist")
            self.assertTrue(False)

        url = reverse('posts:unpost', args={test_post.id,})
        response = client.get(url)

        # Check the response is ok and db reflects change caused by 'unpost'
        self.assertEqual(response.status_code, 200)

        # Check the 'post' does not exist
        try:
            Post.objects.get(poster_id=test_user.id)
        except Post.DoesNotExist:
            self.assertTrue(True)
        
        client.logout()


    def test_delete_post_not_post_author(self):
        test_user, client = self.login()

        url = reverse('posts:create_post')
        response = client.post(url, data={'poster':test_user, 'body':'test body, this can be any text just make sure its nothing important'}, follow=True)

        # Check the response is ok and db reflects change caused by 'post'
        self.assertEqual(response.status_code, 200)

        # Check the 'post' exists
        try:
            test_post = Post.objects.get(poster_id=test_user.id)
        except Post.DoesNotExist:
            print("Post record does not exist")
            self.assertTrue(False)

        client.logout()

        test_user_2_cu = CustomUser.objects.create_user(email="test2@test.com", user_name="test3", password="test2password",date_of_birth=datetime.datetime(1999, 5, 26, 21, 12, 33, 675765, tzinfo=None))
        test_user_2_cu.save()

        # Login as another user and try delete post
        client.login(email="test2@test.com", password="test2password")

        url = reverse('posts:unpost', args={test_post.id,})
        response = client.get(url)

        # Check the response is ok and db reflects no change caused by 'unpost'
        self.assertNotEqual(response.status_code, 200)

        # Check the 'post' exists
        try:
            Post.objects.get(poster_id=test_user.id)
        except Post.DoesNotExist:
            print("Post record does not exist")
            self.assertTrue(False)
        
        client.logout()
        
    def test_create_quote_on_post(self):
        test_user, client = self.login()
        test_post, test_profile = self.create_test_post()

        url = reverse('posts:quote', args={test_post.id,})
        response = client.post(url, data={'poster':test_user, 'body':'test body, this can be any text just make sure its nothing important'}, follow=True)

        # Check the response is ok and db reflects change caused by 'post'
        self.assertEqual(response.status_code, 200)

        # Check the 'quote' exists
        try:
            Quote.objects.get(poster_id=test_user.id)
        except Quote.DoesNotExist:
            print("Quote record does not exist")
            self.assertTrue(False)

        client.logout()

    def test_create_quote_on_quote(self):
        test_user, client = self.login()
        test_quote = self.create_test_quote()

        url = reverse('posts:quote', args={test_quote.id,})
        response = client.post(url, data={'poster':test_user, 'body':'test body, this can be any text just make sure its nothing important'}, follow=True)

        # Check the response is ok and db reflects change caused by 'post'
        self.assertEqual(response.status_code, 200)

        # Check the 'quote' exists
        try:
            Quote.objects.get(poster_id=test_user.id)
        except Quote.DoesNotExist:
            print("Quote record does not exist")
            self.assertTrue(False)

        client.logout()


    def test_create_quote_on_comment(self):
        test_user, client = self.login()
        test_comment = self.create_test_comment()

        url = reverse('posts:quote', args={test_comment.id,})
        response = client.post(url, data={'poster':test_user, 'body':'test body, this can be any text just make sure its nothing important'}, follow=True)

        # Check the response is ok and db reflects change caused by 'post'
        self.assertEqual(response.status_code, 200)

        # Check the 'quote' exists
        try:
            Quote.objects.get(poster_id=test_user.id)
        except Quote.DoesNotExist:
            print("Quote record does not exist")
            self.assertTrue(False)

        client.logout() 


    def test_create_quote_user_not_authenticated(self):
        test_user, client = self.login()
        test_quote = self.create_test_quote()

        client.logout()

        url = reverse('posts:quote', args={test_quote.id,})
        response = client.post(url, data={'poster':test_user, 'body':'test body, this can be any text just make sure its nothing important'}, follow=True)

        # Correctly redirects unauthenticated users to login page
        self.assertNotEqual(response.status_code, 200)


    def test_delete_quote_normal_use(self):
        test_user, client = self.login()
        test_post, test_profile = self.create_test_post()

        url = reverse('posts:quote', args={test_post.id,})
        response = client.post(url, data={'poster':test_user, 'body':'test body, this can be any text just make sure its nothing important'}, follow=True)

        # Check the response is ok and db reflects change caused by 'post'
        self.assertEqual(response.status_code, 200)

        # Check the 'quote' exists
        try:
            test_quote = Quote.objects.get(poster_id=test_user.id)
        except Quote.DoesNotExist:
            print("Post record does not exist")
            self.assertTrue(False)

        url = reverse('posts:unquote', args={test_quote.id,})
        response = client.get(url)

        # Check the response is ok and db reflects change caused by 'unquote'
        self.assertEqual(response.status_code, 200)

        # Check the 'quote' does not exist
        try:
            Quote.objects.get(poster_id=test_user.id)
        except Quote.DoesNotExist:
            self.assertTrue(True)

        client.logout()


    def test_delete_quote_not_quote_author(self):
        test_user, client = self.login()
        test_post, test_profile = self.create_test_post()

        url = reverse('posts:quote', args={test_post.id,})
        response = client.post(url, data={'poster':test_user, 'body':'test body, this can be any text just make sure its nothing important'}, follow=True)

        # Check the response is ok and db reflects change caused by 'post'
        self.assertEqual(response.status_code, 200)

        # Check the 'quote' exists
        try:
            test_quote = Quote.objects.get(poster_id=test_user.id)
        except Quote.DoesNotExist:
            print("Quote record does not exist")
            self.assertTrue(False)

        client.logout()

        test_user_2_cu = CustomUser.objects.create_user(email="test5@test.com", user_name="test6", password="test6password",date_of_birth=datetime.datetime(1999, 5, 26, 21, 12, 33, 675765, tzinfo=None))
        test_user_2_cu.save()

        # Login as another user and try delete quote
        client.login(email="test5@test.com", password="test6password")

        url = reverse('posts:unquote', args={test_quote.id,})
        response = client.get(url)

        # Check the response is not 200 and db reflects no change 
        self.assertNotEqual(response.status_code, 200)

        # Check the 'quote' exists
        try:
            Quote.objects.get(poster_id=test_user.id)
        except Quote.DoesNotExist:
            self.assertTrue(False)

        client.logout()


    def test_create_comment_on_post(self):
        test_user, client = self.login()
        test_post, test_profile = self.create_test_post()

        url = reverse('posts:comment', args={test_post.id,})
        response = client.post(url, data={'poster':test_user, 'body':'test body, this can be any text just make sure its nothing important'}, follow=True)

        # Check the response is ok and db reflects change caused by 'comment'
        self.assertEqual(response.status_code, 200)

        # Check the 'comment' exists
        try:
            Comment.objects.get(poster_id=test_user.id)
        except Comment.DoesNotExist:
            print("Comment record does not exist")
            self.assertTrue(False)

        client.logout()

    
    def test_create_comment_on_quote(self):
        test_user, client = self.login()
        test_quote = self.create_test_quote()

        url = reverse('posts:comment', args={test_quote.id,})
        response = client.post(url, data={'poster':test_user, 'body':'test body, this can be any text just make sure its nothing important'}, follow=True)

        # Check the response is ok and db reflects change caused by 'post'
        self.assertEqual(response.status_code, 200)

        # Check the 'comment' exists
        try:
            Comment.objects.get(poster_id=test_user.id)
        except Comment.DoesNotExist:
            print("Comment record does not exist")
            self.assertTrue(False)

        client.logout()

    
    def test_create_comment_on_comment(self):
        test_user, client = self.login()
        test_comment = self.create_test_comment()

        url = reverse('posts:comment', args={test_comment.id,})
        response = client.post(url, data={'poster':test_user, 'body':'test body, this can be any text just make sure its nothing important'}, follow=True)

        # Check the response is ok and db reflects change caused by 'post'
        self.assertEqual(response.status_code, 200)

        # Check the 'comment' exists
        try:
            Comment.objects.get(poster_id=test_user.id)
        except Comment.DoesNotExist:
            print("Comment record does not exist")
            self.assertTrue(False)

        client.logout()


    def test_create_comment_user_not_authenticated(self):
        test_user, client = self.login()
        test_quote = self.create_test_quote()

        client.logout()

        url = reverse('posts:comment', args={test_quote.id,})
        response = client.post(url, data={'poster':test_user, 'body':'test body, this can be any text just make sure its nothing important'}, follow=True)

        # Correctly redirects unauthenticated users to login page
        self.assertNotEqual(response.status_code, 200) 


    def test_delete_comment_normal_use(self):
        test_user, client = self.login()
        test_post, test_profile = self.create_test_post()

        url = reverse('posts:comment', args={test_post.id,})
        response = client.post(url, data={'poster':test_user, 'body':'test body, this can be any text just make sure its nothing important'}, follow=True)

        # Check the response is ok and db reflects change caused by 'comment'
        self.assertEqual(response.status_code, 200)

        # Check the 'comment' exists
        try:
            test_comment = Comment.objects.get(poster_id=test_user.id)
        except Comment.DoesNotExist:
            print("Post record does not exist")
            self.assertTrue(False)

        url = reverse('posts:uncomment', args={test_comment.id,})
        response = client.get(url)

        # Check the response is ok and db reflects change caused by 'uncomment'
        self.assertEqual(response.status_code, 200)

        # Check the 'comment' does not exist
        try:
            Comment.objects.get(poster_id=test_user.id)
        except Comment.DoesNotExist:
            self.assertTrue(True)

        client.logout()


    def test_delete_comment_not_quote_author(self):
        test_user, client = self.login()
        test_post, test_profile = self.create_test_post()

        url = reverse('posts:comment', args={test_post.id,})
        response = client.post(url, data={'poster':test_user, 'body':'test body, this can be any text just make sure its nothing important'}, follow=True)

        # Check the response is ok and db reflects change caused by 'comment'
        self.assertEqual(response.status_code, 200)

        # Check the 'comment' exists
        try:
            test_comment = Comment.objects.get(poster_id=test_user.id)
        except Comment.DoesNotExist:
            print("Comment record does not exist")
            self.assertTrue(False)

        client.logout()

        test_user_2_cu = CustomUser.objects.create_user(email="test5@test.com", user_name="test6", password="test6password",date_of_birth=datetime.datetime(1999, 5, 26, 21, 12, 33, 675765, tzinfo=None))
        test_user_2_cu.save()

        # Login as another user and try delete comment
        client.login(email="test5@test.com", password="test6password")

        url = reverse('posts:uncomment', args={test_comment.id,})
        response = client.get(url)

        # Check the response is not ok and db reflects no change
        self.assertNotEqual(response.status_code, 200)

        # Check the 'comment' exists
        try:
            Comment.objects.get(poster_id=test_user.id)
        except Comment.DoesNotExist:
            self.assertTrue(False)

        client.logout()


class PostInteractionTests(TestCase):
    
    def login(self):
        self.email = 'test@test.com'
        self.username = 'test1'
        self.password = 'password1'

        user = CustomUser.objects.create_user(email=self.email, user_name=self.username, password=self.password,date_of_birth=datetime.datetime(1999, 5, 26, 21, 12, 33, 675765, tzinfo=None))
        user.save()

        client = Client()
        client.login(email=self.email, password=self.password)
        return user, client
    

    def create_test_post(self):
        test_user = CustomUser.objects.create_user(email='test1@test.com', user_name='test2', password='password2', date_of_birth=datetime.datetime(1999, 5, 26, 21, 12, 33, 675765, tzinfo=None))
        test_user.save()

        profile = UserProfile.objects.get(user=test_user)

        post = Post.objects.create(poster=profile, body='test body, this can be any text just make sure its nothing important')
        post.save()
        return post, profile
    

    def test_create_like_as_normal(self):
        # Create test logins and test post
        test_user, client = self.login()
        test_profile_1 = UserProfile.objects.get(user=test_user)
        test_post, test_profile_2 = self.create_test_post()

        # Check post is not already liked
        self.assertFalse(test_post.likes.contains(test_profile_1))

        # Make request to 'like' post
        url = reverse('posts:like', args=(test_post.id,))
        response = client.get(url)

        # Check the response is ok and db reflects change caused by 'like'
        self.assertEqual(response.status_code, 200)

        # Check the 'like' exists
        self.assertTrue(test_post.likes.contains(test_profile_1))

        client.logout()
    

    def test_create_like_user_not_authenticated(self):
        # Create test logins and test post 
        test_user, client = self.login()
        test_post, test_profile = self.create_test_post()

        client.logout()

        url = reverse('posts:like', args=(test_post.id,))
        response = client.get(url)

        # Correctly redirects unauthenticated users to login page
        self.assertEqual(response.status_code, 302)
           

    def test_delete_like(self):
        # Create test logins and test post
        test_user, client = self.login()
        test_profile_1 = UserProfile.objects.get(user=test_user)
        test_post, test_profile_2 = self.create_test_post()

        # Check post is not already liked
        self.assertFalse(test_post.likes.contains(test_profile_1))

        # Make request to 'like' post
        url = reverse('posts:like', args=(test_post.id,))
        response = client.get(url)

        # Check the response is ok and db reflects change caused by 'like'
        self.assertEqual(response.status_code, 200)

        # Check the 'like' exists
        self.assertTrue(test_post.likes.contains(test_profile_1))

        # Make request to 'unlike' post
        url = reverse('posts:unlike', args=(test_post.id,))
        response = client.get(url)

        # Check the 'like' does not exist anymore
        self.assertFalse(test_post.likes.contains(test_profile_1))
        
        client.logout()


    def test_create_repost_as_normal(self):
        # Create test logins and test post
        test_user, client = self.login()
        test_profile_1 = UserProfile.objects.get(user=test_user)
        test_post, test_profile_2 = self.create_test_post()

        # Check post is not already reposted
        self.assertFalse(test_post.reposts.contains(test_profile_1))

        # Make request to 'repost' post
        url = reverse('posts:repost', args=(test_post.id,))
        response = client.get(url)

        # Check the response is ok and db reflects change caused by 'repost'
        self.assertEqual(response.status_code, 200)

        # Check the 'repost' exists
        self.assertTrue(test_post.reposts.contains(test_profile_1))

        client.logout()


    def test_create_repost_user_not_authenticated(self):
        # Create test logins and test post 
        test_user, client = self.login()
        test_post, test_profile = self.create_test_post()

        client.logout()

        url = reverse('posts:repost', args=(test_post.id,))
        response = client.get(url)

        # Correctly redirects unauthenticated users to login page
        self.assertEqual(response.status_code, 302)


    def test_delete_repost(self):
        # Create test logins and test post
        test_user, client = self.login()
        test_profile_1 = UserProfile.objects.get(user=test_user)
        test_post, test_profile_2 = self.create_test_post()

        # Check post is not already reposted
        self.assertFalse(test_post.reposts.contains(test_profile_1))

        # Make request to 'repost' post
        url = reverse('posts:repost', args=(test_post.id,))
        response = client.get(url)

        # Check the response is ok and db reflects change caused by 'repost'
        self.assertEqual(response.status_code, 200)

        # Check the 'repost' exists
        self.assertTrue(test_post.reposts.contains(test_profile_1))

        # Make request to 'unrepost' post
        url = reverse('posts:unrepost', args=(test_post.id,))
        response = client.get(url)

        # Check the 'repost' does not exist anymore
        self.assertFalse(test_post.reposts.contains(test_profile_1))
        
        client.logout()


    def test_create_bookmark_as_normal(self):
        # Create test logins and test post
        test_user, client = self.login()
        test_profile_1 = UserProfile.objects.get(user=test_user)
        test_post, test_profile_2 = self.create_test_post()

        # Check post is not already bookmarked
        self.assertFalse(test_post.bookmarks.contains(test_profile_1))

        # Make request to 'bookmark' post
        url = reverse('posts:bookmark', args=(test_post.id,))
        response = client.get(url)

        # Check the response is ok and db reflects change caused by 'bookmark'
        self.assertEqual(response.status_code, 200)

        # Check the 'bookmark' exists
        self.assertTrue(test_post.bookmarks.contains(test_profile_1))

        client.logout()


    def test_create_bookmark_not_authenticated(self):
        # Create test logins and test post 
        test_user, client = self.login()
        test_post, test_profile = self.create_test_post()

        client.logout()

        url = reverse('posts:bookmark', args=(test_post.id,))
        response = client.get(url)

        # Correctly redirects unauthenticated users to login page
        self.assertEqual(response.status_code, 302)


    def test_delete_bookmark(self):
        # Create test logins and test post
        test_user, client = self.login()
        test_profile_1 = UserProfile.objects.get(user=test_user)
        test_post, test_profile_2 = self.create_test_post()

        # Check post is not already bookmarked
        self.assertFalse(test_post.bookmarks.contains(test_profile_1))

        # Make request to 'bookmark' post
        url = reverse('posts:bookmark', args=(test_post.id,))
        response = client.get(url)

        # Check the response is ok and db reflects change caused by 'bookmark'
        self.assertEqual(response.status_code, 200)

        # Check the 'bookmark' exists
        self.assertTrue(test_post.bookmarks.contains(test_profile_1))

        # Make request to 'unbookmark' post
        url = reverse('posts:unbookmark', args=(test_post.id,))
        response = client.get(url)

        # Check the 'bookmark' does not exist anymore
        self.assertFalse(test_post.bookmarks.contains(test_profile_1))
        
        client.logout()
