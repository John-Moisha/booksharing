from django.urls import path
from books import views

app_name = 'books'

urlpatterns = [
    path('list/', views.BookList.as_view(), name='books-list'),
    path('my-list/', views.MyBookList.as_view(), name='my-books-list'),
    path('create/', views.BookCreate.as_view(), name='book-create'),
    path('update/<int:pk>/', views.BookUpdate.as_view(), name='book-update'),
    path('delete/<int:pk>/', views.BookDelete.as_view(), name='book-delete'),

    path('create/book/request/<int:book_id>/', views.RequestBookCreate.as_view(),
         name='create-book-request'),
    path('my-list/my-requested-books/', views.MyRequestedBooks.as_view(),
         name='my-requested-books'),
    path('my-list/requested-books/', views.RequestedBooks.as_view(),
         name='requested-books'),
    path('requested-books/confirm/<int:request_id>/', views.RequestBookConfirm.as_view(),
         name='requested-books-confirm'),
    path('requested-books/reject/<int:request_id>/', views.RequestBookReject.as_view(),
         name='requested-books-reject'),
    path('requested-books/sent-via-email/<int:request_id>/', views.RequestBookSentViaEmail.as_view(),
         name='sent-via-email'),
    path('requested-books/book-received/<int:request_id>/', views.RequestBookReceivedBook.as_view(),
         name='book-received'),
    path('requested-books/sent-back-to-owner/<int:request_id>/', views.RequestBookSentBackToOwner.as_view(),
         name='sent-back-to-owner'),
    path('requested-books/owner-received/<int:request_id>/', views.RequestBookOwnerReceivedBack.as_view(),
         name='owner-received'),

    path('author/list/', views.AuthorList.as_view(), name='authors-list'),
    path('author/my-list/', views.MyAuthorList.as_view(), name='my-authors-list'),
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/update/<int:pk>/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/delete/<int:pk>/', views.AuthorDelete.as_view(), name='author-delete'),

    path('download-csv/', views.DownloadCSVBooksView.as_view(), name='download-csv'),
    path('download-xlsx/', views.DownloadXLSXBooksView.as_view(), name='download-xlsx'),
    path('author/download-csv/', views.DownloadCSVAuthorsView.as_view(), name='authors-download-csv'),
    path('author/download-xlsx/', views.DownloadXLSXAuthorsView.as_view(), name='authors-download-xlsx'),
]
