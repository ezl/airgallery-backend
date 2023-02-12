import django_filters
from galleries.models import Image

class ImageFilter(django_filters.rest_framework.FilterSet):
    gallery = django_filters.CharFilter(required=True, method="filter_gallery_id")

    class Meta:
        model = Image
        fields = []


    def filter_gallery_id(self, queryset, name, value):
        if value == 'current_user':
            gallery = Gallery.objects.filter(user=self.request.user).first()
            return queryset.filter(gallery=gallery)
        if value.isdigit():
            return queryset.filter(gallery__id=value)
        else:
            return queryset.filter(gallery__slug=value)
