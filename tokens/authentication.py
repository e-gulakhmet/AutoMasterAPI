from django.utils.translation import gettext_lazy as _
from django.core.cache import cache
from rest_framework_simplejwt.authentication import JWTAuthentication as BaseJWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken


class JWTAuthentication(BaseJWTAuthentication):
    def get_user(self, validated_token):
        """
        Attempts to find and return a user using the given validated token.
        """
        user_id, email = None, None
        user = None

        try:
            user_id = validated_token['user_id']
        except KeyError:
            try:
                email = validated_token['email']
            except KeyError:
                raise InvalidToken(_('Token contained no recognizable user identification'))

        if user_id is not None:
            try:
                user = self.user_model.objects.get(pk=user_id)
            except self.user_model.DoesNotExist:
                raise AuthenticationFailed(_('User not found'), code='user_not_found')
        elif email is not None:
            try:
                user = self.user_model.objects.get(email=email)
            except self.user_model.DoesNotExist:
                raise AuthenticationFailed(
                    _('User not found'), code='user_not_found')

        if not user.is_active:
            raise AuthenticationFailed(_('User is inactive'), code='user_inactive')

        # Set online status
        cache.set(user.pk, 1, timeout=600)

        return user
