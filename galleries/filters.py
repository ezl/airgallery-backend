import django_filters
from django.contrib.auth.models import User
from galleries.models import Image, Gallery

class ImageFilter(django_filters.rest_framework.FilterSet):
    # TODO: Question for robert - conventionwise, would i want
    # to call this GalleryFilter or something to indicate that
    # this filter, for images, is actually doing a filter operation
    # that is limiting it to the gallery?
    # presumably there can be multiple ImageFilters that do
    # different things?
    gallery = django_filters.CharFilter(required=True, method="filter_gallery_id")

    class Meta:
        model = Image
        fields = []

    def filter_gallery_id(self, queryset, name, value):
        '''
        if value == 'current_user':
            gallery = Gallery.objects.filter(user=self.request.user).first()
            return queryset.filter(gallery=gallery)
        '''
        if value.isdigit():
            return queryset.filter(gallery__id=value)
        else:
            return queryset.filter(gallery__slug=value)

class GalleryFilter(django_filters.rest_framework.FilterSet):
    user = django_filters.CharFilter(required=False, method='filter_user')

    class Meta:
        model = Gallery
        fields = []

    def filter_user(self, queryset, name, value):
        if value == 'request.user':
            user = User.objects.get(id=self.request.user.id)
            return queryset.filter(user=user)
