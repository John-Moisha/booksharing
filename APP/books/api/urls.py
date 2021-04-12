from books.api import view
from rest_framework.routers import DefaultRouter


app_name = 'books-api'

router = DefaultRouter()

router.register('books', view.BookModelViewSet, basename='book')
router.register('authors', view.AuthorModelViewSet, basename='author')
router.register('categories', view.CategoryModelViewSet, basename='category')

urlpatterns = router.urls
