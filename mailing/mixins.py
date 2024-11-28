from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied


class UserObjectMixin(LoginRequiredMixin, PermissionRequiredMixin):
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not obj.user == self.request.user:
            raise PermissionDenied('You do not have permission to access this object.')
        return obj

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class UserMailingObjectMixin(LoginRequiredMixin, PermissionRequiredMixin):
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not object.mailing.user == self.request.user:
            raise PermissionDenied('You do not have permission to access this object.')
        return obj
