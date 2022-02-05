import random
import os
from abc import ABC, abstractmethod
from enum import Enum

from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework.test import APIClient
from django.core.files import File
from django.conf import settings

import utils.random
from categories.models import CategoryToContentRelation, Category
from favorites.models import Favorite
from main.enums import UserAgeType
from payments.enums import PaymentSystemTypes
from poll.models import Poll, PollOption, PollOptionMark
from publications.models import Link
from purchases.models import Purchase
from shop.models import CatalogProduct, Catalog
from stats.models import Expand
from utils.helper import get_file_rb
from search.models import SearchHistory

from chats.models import ChatRoom, ChatRoomMessage, ChatCustomer
from users.models import User, Subscription, Mute, Block
from users.tokens.serializers import TokenObtainPairSerializer
from album.models import Album
from utils.vcr import VCRMixin
from streams.models import Stream, Ticket
from tags.models import Tag, TagToContentRelation, ContentUserTag
from comments.models import Comment
from likes.models import Like
from views.models import View
from subscriptions.services import SubscriptionService
from posts.models import Post
from posts.documents import PostDocument
from payments.services import PaymentService, BasePaymentSystemService
from file_manager.models import Attachment, AttachmentToContentRelation, ImageProperties
from fundraising.models import Fundraising, FundraisingMilestone
from donations.models import Donate
from notifications.models import Notification
from notifications.enums import NotificationsCodes
from chats.enums import ChatTypes, ChatCustomerTypes
from stories.models import Story


class UserFactoryMixin:
    USER_PASSWORD = 'sdw332!4TdSD'

    @staticmethod
    def __random_char(length=10, repeat=1):
        return ''.join(utils.random.random_simple_string(length) for _ in range(repeat))

    def create_user(self, email: str, first_name: str, last_name: str, **kwargs) -> 'User':
        if len(first_name) == 0:
            first_name = 'None'
        if len(last_name) == 0:
            last_name = 'None'
        user = User.objects.create_user(email=email, password=self.USER_PASSWORD, first_name=first_name,
                                        last_name=last_name, **kwargs)
        user.save()
        return user

    def create_random_user(self, **kwargs) -> 'User':
        return self.create_user(
            email=self.__random_char() + "@gmail.com",
            first_name=self.__random_char(),
            last_name=self.__random_char(),
            **kwargs
        )

    @staticmethod
    def create_client_with_auth(user: 'User') -> APIClient:
        token = TokenObtainPairSerializer.get_token(user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer %s' % token.access_token)
        return client


class IsAuthClientTestCase(UserFactoryMixin, ABC):
    user: User
    client: APIClient

    staff_user: User
    staff_client: APIClient

    anonymous_client: APIClient

    def setUp(self):
        self.user = self.create_random_user()
        self.client = self.create_client_with_auth(self.user)

        self.staff_user = self.create_random_user(is_staff=True)
        self.staff_client = self.create_client_with_auth(user=self.staff_user)

        self.anonymous_client = self.client_class()


class TestDataService(UserFactoryMixin):
    DEFAULT_ENTITIES_COUNT = 10

    used_users = set([])
    used_verified_users = set([])
    used_acp_users = set([])

    def _get_next_random_user(self) -> User:
        """ Return random user excluding already selected """

        users = set(User.objects.all())
        to_select = users - self.used_users
        if not to_select:
            to_select = users
            self.used_users = set([])
        choice = random.choice(list(to_select))
        self.used_users.add(choice)
        return choice

    def create_users(self, count: int = DEFAULT_ENTITIES_COUNT):
        for _ in range(count):
            self.create_random_user()


def get_test_jpg_picture() -> File:
    return get_file_rb(filename='test_picture.jpg', path=settings.TEST_FILES_ROOT)


def get_test_png_picture() -> File:
    return get_file_rb(filename='test_picture.png', path=settings.TEST_FILES_ROOT)
