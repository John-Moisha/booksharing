from django import forms

from books.models import Book, Author


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = (
            'author',
            'title',
            'category',
            'publish_year',
            'review',
            'condition',
        )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user

        if commit:
            instance.save()

        return instance


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = (
            'first_name',
            'last_name',
            'date_of_birth',
            'date_of_death',
            'country',
            'gender',
            'native_language',
        )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user

        if commit:
            instance.save()

        return instance


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
