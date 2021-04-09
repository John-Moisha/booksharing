from django.urls import path
from books.api import view
from rest_framework.routers import DefaultRouter


app_name = 'books-api'

router = DefaultRouter()

router.register('books', view.BookModelViewSet, basename='book')
router.register('author', view.BookModelViewSet, basename='author')
router.register('category', view.BookModelViewSet, basename='category')

urlpatterns = router.urls