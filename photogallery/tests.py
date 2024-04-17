from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from photogallery.models import Photo, Comment


class TesthomeView(TestCase):
    def test_home_view(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")


class TestSignupView(TestCase):
    def test_signup_view(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "signup.html")

    def test_signup_new_user(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "testuser",
                "password1": "test-password123",
                "password2": "test-password123",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="testuser").exists())


class TestLoginView(TestCase):
    def test_login_view(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")


class TestCreatePostView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_create_post_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("add_photo"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "add_photo.html")


class TestDeletePostView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.post = Photo.objects.create(
            user=self.user, image="Test Post", comment="This is a test post"
        )

    def test_delete_post_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("delete_photo", kwargs={"pk": self.post.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Photo.objects.filter(description="This is a test post").exists()
        )


class TestPhotoModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_photo_creation(self):
        cat_post = Photo.objects.create(
            user=self.user,
            image="C:/Users/alanc/OneDrive/Images/cute-cat.jpg",
            description="Test description",
        )
        self.assertEqual(cat_post.user, self.user)
        self.assertEqual(cat_post.image, "C:/Users/alanc/OneDrive/Images/cute-cat.jpg")
        self.assertEqual(cat_post.description, "Test description")


class TestCommentModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.cat_post = Photo.objects.create(
            user=self.user,
            image="C:/Users/alanc/OneDrive/Images/cute-cat.jpg",
            description="Test description",
        )

    def test_comment_creation(self):
        comment = Comment.objects.create(
            user=self.user, photo=self.cat_post, text="Test comment"
        )
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.photo, self.cat_post)
        self.assertEqual(comment.text, "Test comment")
