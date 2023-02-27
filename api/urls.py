from django.urls import path

from api.views.connect_storage_backend import ConnectStorageBackend
from api.views.current_user import CurrentUser
from api.views.drive_upload_image import DriveUploadImage
from api.views.gallery_images import GalleryImages
from api.views.single_gallery import SingleGallery
from api.views.current_user_gallery import CurrentUserGallery
from api.views.current_user_gallery_images import CurrentUserGalleryImages
from api.views.toggle_gallery_publication import ToggleGalleryPublication



urlpatterns = [
    path('storage-backends/connect', ConnectStorageBackend.as_view()),
    path('upload/drive', DriveUploadImage.as_view()),

    # use a gallery
    # path('galleries/by-slug/<str:slug>', SingleGallery.as_view()), #replacement view has been created (not in use)
    # path('galleries/<int:id>/toggle-publication', ToggleGalleryPublication.as_view()), # replacement view has been created (and is in use)

    # use an image viewset with different filtering
    # get (request.user, gallery_id)
    # path('galleries/<int:id>/images', GalleryImages.as_view()),
    # path('auth/user/gallery/images', CurrentUserGalleryImages.as_view()),

    path('auth/user', CurrentUser.as_view()),
    # path('auth/user/gallery', CurrentUserGallery.as_view()),
]
