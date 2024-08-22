import datetime  

from django.test import TestCase
from django.test.client import Client
from django.urls import reverse 

from interactions.models import Like
from interactions.models import Repost
from interactions.models import Bookmark
from posts.models import Comment
from posts.models import Post
from posts.models import Quote    
from relations.models import Follow
from users.models import CustomUser
from user_profile.models import UserProfile

class ProfileViewTests(TestCase):
    def login(self):
        self.email = 'test@test.com'
        self.username = 'test1'
        self.password = 'password1'

        user = CustomUser.objects.create_user(email=self.email, user_name=self.username, password=self.password,date_of_birth=datetime.datetime(1999, 5, 26, 21, 12, 33, 675765, tzinfo=None))
        user.save()

        client = Client()
        client.login(email=self.email, password=self.password)
        
        user_profile = UserProfile.objects.get(user=user)
        user_profile.bio = "I'm new here ! :)"
        user_profile.location = "Mars"
        user_profile.display_name = "New User"
        user_profile.save()

        return user_profile, client
    
    def test_view_profile(self):
        test_user, client = self.login()

        url = reverse('profile:home', args=(test_user.id,))
        response = client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["bio"], "I'm new here ! :)")
        self.assertEqual(response.context["location"], "Mars")
        self.assertEqual(response.context["display_name"], "New User")
        # Need to add other profile information to testing framework when that is complete
        client.logout()

    def test_view_following(self):
        test_user, client = self.login()

        url = reverse('profile:following', args=(test_user.id,))
        response = client.get(url)

        # check the response is ok and the latest following list is empty
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['latest_following_list']) # empty dict resolves to false in python

        # create second test user 
        test_user2_cu = CustomUser.objects.create_user(email='test2@test.com', user_name='test2', password='test1password',date_of_birth=datetime.datetime(1999, 5, 26, 21, 12, 33, 675765, tzinfo=None))
        test_user2_cu.save()

        test_user2 = UserProfile.objects.get(user=test_user2_cu)

        # follow second test user with authenticated user
        new_follow = Follow(
            follower = test_user,
            following = test_user2
        )
        new_follow.save()

        # check following again to see test_user2 is being followed
        url = reverse('profile:following', args=(test_user.id,))
        response = client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['latest_following_list'][0].id, 
        test_user2.id) 

        client.logout()

    def test_view_followers(self):
        test_user, client = self.login()

        url = reverse('profile:followers', args=(test_user.id,))
        response = client.get(url)

        # check the response is ok and the latest followers list is empty
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['latest_followers_list']) # empty dict resolves to false in python

        # create second test user 
        test_user2_cu = CustomUser.objects.create_user(email='test3@test.com', user_name='test3', password='test2password',date_of_birth=datetime.datetime(1999, 5, 26, 21, 12, 33, 675765, tzinfo=None))
        test_user2_cu.save()

        test_user2 = UserProfile.objects.get(user=test_user2_cu)

        # follow authenticated user with second test user
        new_follow = Follow(
            follower = test_user2,
            following = test_user
        )
        new_follow.save()

        # check followers again to see test_user is being followed by test_user2
        url = reverse('profile:followers', args=(test_user.id,))
        response = client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['latest_followers_list'][0].id, 
        test_user2.id) 

        client.logout()

    def test_view_user_posts(self):
        test_user, client = self.login()

        url = reverse('profile:posts', args=(test_user.id,))
        response = client.get(url)

        # check the response is ok and the latest posts list is empty
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['latest_posts_list']) # empty dict resolves to false in python

        # create post 
        new_post = Post.objects.create(poster=test_user, body='testbody, this can be any text just make sure its nothing important')
        new_post.save()

        # check the user posts again and we should see the post we just created above
        url = reverse('profile:posts', args=(test_user.id,))
        response = client.get(url)

        # check the response is ok and the latest posts list has new post
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['latest_posts_list'][0].poster_id, test_user.id)
        self.assertEqual(response.context["latest_posts_list"][0].body, "testbody, this can be any text just make sure its nothing important")

        client.logout() 


    def test_view_user_quotes(self):
        test_user, client = self.login()

        url = reverse('profile:quotes', args=(test_user.id,))
        response = client.get(url)

        # check the response is ok and the latest posts list is empty
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['latest_quotes_list']) # empty dict resolves to false in python

        # create post 
        new_post = Post.objects.create(poster=test_user, body='testbody, this can be any text just make sure its nothing important')
        new_post.save()

        # create quote
        new_quote = Quote.objects.create(poster=test_user, body='testbody, this can be any text just make sure its nothing important', quote_post=new_post)
        new_quote.save()

        # check the user quotes again and we should see the quotes we just created above
        url = reverse('profile:quotes', args=(test_user.id,))
        response = client.get(url)

        # check the response is ok and the latest quotes list has new quote
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['latest_quotes_list'][0].poster_id, test_user.id)
        self.assertEqual(response.context["latest_quotes_list"][0].body, "testbody, this can be any text just make sure its nothing important")

        client.logout() 


    def test_view_user_comments(self):
        test_user, client = self.login()

        url = reverse('profile:comments', args=(test_user.id,))
        response = client.get(url)

        # check the response is ok and the latest comments list is empty
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['latest_comments_list']) # empty dict resolves to false in python

        # create post 
        new_post = Post.objects.create(poster=test_user, body='testbody, this can be any text just make sure its nothing important')
        new_post.save()

        # create comment
        new_comment = Comment.objects.create(poster=test_user, body='testbody, this can be any text just make sure its nothing important', reply_post=new_post)
        new_comment.save()

        # check the user comments again and we should see the comment we just created above
        url = reverse('profile:comments', args=(test_user.id,))
        response = client.get(url)

        # check the response is ok and the latest comments list has new comment
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['latest_comments_list'][0].poster_id, test_user.id)
        self.assertEqual(response.context["latest_comments_list"][0].body, "testbody, this can be any text just make sure its nothing important")

        client.logout() 

    def test_view_user_reposts(self):
        test_user, client = self.login()

        url = reverse('profile:reposts', args=(test_user.id,))
        response = client.get(url)

        # check the response is ok and the latest reposts list is empty
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['latest_reposts_list']) # empty dict resolves to false in python

        # create post 
        new_post = Post.objects.create(poster=test_user, body='testbody, this can be any text just make sure its nothing important')
        new_post.save()

        # create repost
        new_repost = Repost.objects.create(poster=test_user, reposter=test_user, post=new_post)
        new_repost.save()

        # check the user reposts again and we should see the repost we just created above
        url = reverse('profile:reposts', args=(test_user.id,))
        response = client.get(url)

        # check the response is ok and the latest reposts list has new repost
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['latest_reposts_list'][0].poster_id, test_user.id)
        self.assertEqual(response.context["latest_reposts_list"][0].body, "testbody, this can be any text just make sure its nothing important")

        client.logout() 

    def test_view_user_likes(self):
        test_user, client = self.login()

        url = reverse('profile:likes', args=(test_user.id,))
        response = client.get(url)

        # check the response is ok and the latest likes list is empty
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['latest_likes_list']) # empty dict resolves to false in python

        # create post 
        new_post = Post.objects.create(poster=test_user, body='testbody, this can be any text just make sure its nothing important')
        new_post.save()

        # create likes
        new_like = Like.objects.create(poster=test_user, liker=test_user, post=new_post)
        new_like.save()

        # check the user likes again and we should see the like we just created above
        url = reverse('profile:likes', args=(test_user.id,))
        response = client.get(url)

        # check the response is ok and the latest likes list has new like
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['latest_likes_list'][0].poster_id, test_user.id)
        self.assertEqual(response.context["latest_likes_list"][0].body, "testbody, this can be any text just make sure its nothing important")

        client.logout()

    def test_view_user_bookmarks(self):
        test_user, client = self.login()

        url = reverse('profile:bookmarks')
        response = client.get(url)

        # check the response is ok and the latest bookmarks list is empty
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['latest_bookmarks_list']) # empty dict resolves to false in python

        # create post 
        new_post = Post.objects.create(poster=test_user, body='testbody, this can be any text just make sure its nothing important')
        new_post.save()

        # create bookmark
        new_bookmark = Bookmark.objects.create(poster=test_user, bookmarker=test_user, post=new_post)
        new_bookmark.save()

        # check the user likes again and we should see the like we just created above
        url = reverse('profile:bookmarks')
        response = client.get(url)

        # check the response is ok and the latest likes list has new like
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['latest_bookmarks_list'][0].poster_id, test_user.id)
        self.assertEqual(response.context["latest_bookmarks_list"][0].body, "testbody, this can be any text just make sure its nothing important")

        client.logout()

class ProfileEditTests(TestCase):
    def login(self):
        self.email = 'test@test.com'
        self.username = 'test1'
        self.password = 'password1'

        user = CustomUser.objects.create_user(email=self.email, user_name=self.username, password=self.password,date_of_birth=datetime.datetime(1999, 5, 26, 21, 12, 33, 675765, tzinfo=None))
        user.save()

        client = Client()
        client.login(email=self.email, password=self.password)
        
        user_profile = UserProfile.objects.get(user=user)
        user_profile.bio = "I'm new here ! :)"
        user_profile.location = "Mars"
        user_profile.display_name = "New User"
        user_profile.save()

        return user_profile, client
    
    def test_create_follow_normal_use(self):
        test_user, client = self.login()

        # create second test user 
        test_user2_cu = CustomUser.objects.create_user(email='test2@test.com', user_name='test2', password='test1password',date_of_birth=datetime.datetime(1999, 5, 26, 21, 12, 33, 675765, tzinfo=None))
        test_user2_cu.save()

        test_user2 = UserProfile.objects.get(user=test_user2_cu)

        # attempt to follow second test user
        url = reverse('profile:create_follow', args=(test_user2.id,))
        response = client.get(url)

        # response should be ok and db should reflect new follow
        self.assertEqual(response.status_code, 200)

        # check the 'follow' exists
        try:
            Follow.objects.get(follower=test_user, following=test_user2)
        # catch the exception and fail test if follow does not exist
        except Follow.DoesNotExist:
            print("Follow record does not exist")
            self.assertTrue(False)

        client.logout()


    def test_create_follow_try_follow_self(self):
        test_user, client = self.login()

        # attempt to follow own account 
        url = reverse('profile:create_follow', args=(test_user.id,))
        response = client.get(url)

        # response should be not be 200 and db should not reflect new follow
        self.assertNotEqual(response.status_code, 200)

        # check the 'follow' does not exist
        try:
            Follow.objects.get(follower=test_user, following=test_user)
            self.assertTrue(False)
        # catch the exception and fail test if follow does exist
        except Follow.DoesNotExist:
            self.assertTrue(True)

        client.logout()

    def test_delete_follow_normal_use(self):
        test_user, client = self.login()

        # create second test user 
        test_user2_cu = CustomUser.objects.create_user(email='test2@test.com', user_name='test2', password='test1password',date_of_birth=datetime.datetime(1999, 5, 26, 21, 12, 33, 675765, tzinfo=None))
        test_user2_cu.save()

        test_user2 = UserProfile.objects.get(user=test_user2_cu)

        # attempt to follow second test user
        url = reverse('profile:create_follow', args=(test_user2.id,))
        response = client.get(url)

        # response should be ok and db should reflect new follow
        self.assertEqual(response.status_code, 200)

        # check the 'follow' exists
        try:
            Follow.objects.get(follower=test_user, following=test_user2)
        # catch the exception and fail test if follow does not exist
        except Follow.DoesNotExist:
            print("Follow record does not exist")
            self.assertTrue(False)

        # attempt to unfollow second test user
        url= reverse('profile:delete_follow', args=(test_user2.id,))
        response = client.get(url)

        # response should be 200 and db should reflect change
        self.assertEqual(response.status_code, 200)

        # check the 'follow' does not  exist
        try:
            Follow.objects.get(follower=test_user, following=test_user2)
            self.assertTrue(False)
        # catch the exception and fail test if follow does exist
        except Follow.DoesNotExist:
            self.assertTrue(True)
        
        client.logout()

    def test_delete_follow_when_not_following(self):
        test_user, client = self.login()

        # create second test user 
        test_user2_cu = CustomUser.objects.create_user(email='test2@test.com', user_name='test2', password='test1password',date_of_birth=datetime.datetime(1999, 5, 26, 21, 12, 33, 675765, tzinfo=None))
        test_user2_cu.save()

        test_user2 = UserProfile.objects.get(user=test_user2_cu)

        # attempt to unfollow second test user
        url= reverse('profile:delete_follow', args=(test_user2.id,))
        response = client.get(url)

        # response should not be 200 and db should reflect no change
        self.assertNotEqual(response.status_code, 200)

        # check the 'follow' does not  exist
        try:
            Follow.objects.get(follower=test_user, following=test_user2)
            self.assertTrue(False)
        # catch the exception and fail test if follow does exist
        except Follow.DoesNotExist:
            self.assertTrue(True)

        client.logout()

    def test_remove_follow_normal_use(self):
        test_user, client = self.login()

        # create second test user 
        test_user2_cu = CustomUser.objects.create_user(email='test2@test.com', user_name='test2', password='test1password',date_of_birth=datetime.datetime(1999, 5, 26, 21, 12, 33, 675765, tzinfo=None))
        test_user2_cu.save()

        test_user2 = UserProfile.objects.get(user=test_user2_cu)

        # attempt to follow second test user
        url = reverse('profile:create_follow', args=(test_user2.id,))
        response = client.get(url)

        # response should be ok and db should reflect new follow
        self.assertEqual(response.status_code, 200)

        # check the 'follow' exists
        try:
            Follow.objects.get(follower=test_user, following=test_user2)
        # catch the exception and fail test if follow does not exist
        except Follow.DoesNotExist:
            print("Follow record does not exist")
            self.assertTrue(False)

        # attempt to remove second test user as follower
        url= reverse('profile:remove_follow', args=(test_user2.id,))
        response = client.get(url)

        # response should be ok and db should reflect removal
        self.assertEqual(response.status_code, 200)

        # check the 'follow' does not  exist
        try:
            Follow.objects.get(follower=test_user, following=test_user2)
            self.assertTrue(False)
        # catch the exception and fail test if follow does exist
        except Follow.DoesNotExist:
            self.assertTrue(True)

        client.logout()

    def test_remove_follow_when_not_follower(self):
        test_user, client = self.login()

        # create second test user 
        test_user2_cu = CustomUser.objects.create_user(email='test2@test.com', user_name='test2', password='test1password',date_of_birth=datetime.datetime(1999, 5, 26, 21, 12, 33, 675765, tzinfo=None))
        test_user2_cu.save()

        test_user2 = UserProfile.objects.get(user=test_user2_cu)

        # attempt to unfollow second test user
        url= reverse('profile:remove_follow', args=(test_user2.id,))
        response = client.get(url)

        # response should not be 200 and db should reflect no change
        self.assertNotEqual(response.status_code, 200)

        # check the 'follow' does not  exist
        try:
            Follow.objects.get(follower=test_user, following=test_user2)
            self.assertTrue(False)
        # catch the exception and fail test if follow does exist
        except Follow.DoesNotExist:
            self.assertTrue(True)

        client.logout()

