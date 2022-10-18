import shutil
import tempfile

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from posts.models import Group, Post, User

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=f'{settings.BASE_DIR}/TEMP')


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class BaseCaseForTests(TestCase):
    NAME = 'HasNoName'
    NAME_ANOTHER = 'HasNameAlian'
    NAME_THIRD = 'HasNameThird'
    SLUG = 'test-slug'
    SLUG_ANOTHER = 'test-slug-alian'
    LOGIN_URL = reverse('users:login')
    MAIN_PAGE_URL = reverse('posts:index')
    FOLLOW_MAIN_PAGE_URL = reverse('posts:follow_index')
    PROFILE_URL = reverse('posts:profile', args=[NAME])
    ANOTHER_PROFILE_URL = reverse('posts:profile', args=[NAME_ANOTHER])
    FOLLOW_URL = reverse('posts:profile_follow', args=[NAME])
    UNFOLLOW_URL = reverse('posts:profile_unfollow', args=[NAME])
    POST_CREATE_URL = reverse('posts:post_create')
    POST_CREATE_URL_REDIRECT = f'{LOGIN_URL}?next={POST_CREATE_URL}'
    GROUP_POSTS_URL = reverse('posts:group_posts', args=[SLUG])
    ANOTHER_GROUP_POSTS_URL = reverse(
        'posts:group_posts', args=[SLUG_ANOTHER]
    )
    GIF = (
        b'\x47\x49\x46\x38\x39\x61\x02\x00'
        b'\x01\x00\x80\x00\x00\x00\x00\x00'
        b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
        b'\x00\x00\x00\x2C\x00\x00\x00\x00'
        b'\x02\x00\x01\x00\x00\x02\x02\x0C'
        b'\x0A\x00\x3B'
    )

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=cls.NAME)
        cls.user_another = User.objects.create_user(
            username=cls.NAME_ANOTHER
        )
        cls.user_third = User.objects.create_user(username=cls.NAME_THIRD)
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug=cls.SLUG,
            description='Тестовое описание'
        )
        cls.group_another = Group.objects.create(
            title='Тестовая группа чужая',
            slug=cls.SLUG_ANOTHER,
            description='Тестовое описание чужой группы'
        )
        cls.GIF_FILE = SimpleUploadedFile(
            name='small.gif', content=cls.GIF, content_type='image/gif'
        )
        cls.GIF_ANOTHER_FILE = SimpleUploadedFile(
            name='small_another.gif', content=cls.GIF, content_type='image/gif'
        )
        cls.post = Post.objects.create(
            text='Первый пост.',
            author=cls.user,
            group=cls.group,
            image=cls.GIF_FILE
        )
        cls.POST_EDIT_URL = reverse('posts:post_edit', args=[cls.post.id])
        cls.POST_DETAIL_URL = reverse('posts:post_detail', args=[cls.post.id])
        cls.POST_EDIT_URL_REDIRECT = (
            f'{cls.LOGIN_URL}?next={cls.POST_EDIT_URL}'
        )
        cls.POST_COMMENT = reverse('posts:add_comment', args=[cls.post.id])

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.guest = Client()
        self.author = Client()
        self.author.force_login(self.user)
        self.another = Client()
        self.another.force_login(self.user_another)
        self.third = Client()
        self.third.force_login(self.user_third)
