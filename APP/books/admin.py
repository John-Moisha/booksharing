from django.contrib import admin
from books.models import RequestBook, Author, Book


class RequestBookAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'recipient',
        'book',
        'created',
        'status',
    )
    readonly_fields = ('recipient', 'book')
    list_filter = ('status', 'created', )
    search_fields = ('recipient__username', 'recipient__last_name')
    # list_select_related = ('recipient', 'book')  # objects.select_related('recipient', 'book')

    # def get_readonly_fields(self, request, obj=None):
    #     readonly_fields = super().get_readonly_fields()

    def has_delete_permission(self, request, obj=None):
        return False


class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'country',
    )
    readonly_fields = ('first_name', 'last_name', 'country')
    list_filter = ('country', )
    search_fields = ('first_name', 'last_name', 'country')

    def has_delete_permission(self, request, obj=None):
        return False


class BookAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'author',
    )
    readonly_fields = ('title', )
    list_filter = ('category', )
    search_fields = ('title', 'category', 'author')

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(RequestBook, RequestBookAdmin)
