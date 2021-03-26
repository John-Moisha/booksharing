from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, CreateView, RedirectView, View
from django.urls import reverse_lazy
from annoying.functions import get_object_or_None

from accounts.forms import SighUpForm
from accounts.models import User, ContactUs
from accounts.tasks import send_contact_us_email

from .tokens import account_activation_token

class MyProfileView(LoginRequiredMixin, UpdateView):
    queryset = User.objects.all()
    success_url = reverse_lazy('index')
    fields = (
        'first_name',
        'last_name',
        'avatar',
    )

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset.filter(pk=self.request.user.pk)

    def get_object(self, queryset=None):
        return self.request.user


class ContactUsView(CreateView):
    model = ContactUs
    success_url = reverse_lazy('index')
    fields = (
        'full_name',
        'contact_to_email',
        'message',
    )

    def form_valid(self, form):

        response = super().form_valid(form)
        send_contact_us_email.delay(form.cleaned_data)
        # send_contact_us_email.apply_async(
        #     args=(form.cleaned_data, ), countdown=10)

        return response


class SignUpView(CreateView):
    model = User
    success_url = reverse_lazy('index')
    form_class = SighUpForm
    template_name = 'accounts/signup.html'

# def signup2(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#             return redirect('index')
#     else:
#         form = UserCreationForm()
#     return render(request, 'accounts/signup2.html', {'form': form})


class ActivateView(RedirectView):
    pattern_name = 'login'

    def get_redirect_url(self, *args, **kwargs):
        username = kwargs.pop('username')
        user = get_object_or_None(User, username=username, is_active=False)
        if user:
            user.is_active = True
            user.save(update_fields=('is_active', ))
            messages.add_message(self.request, messages.INFO, 'Your account is activated!')
        return super().get_redirect_url(*args, **kwargs)


# class ActivateAccountView(View):
#     def get(self, request, uidb64, token):
#         try:
#             uid = force_text(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(pk=uid)
#         except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#             user = None
#
#         if user is not None and account_activation_token.check_token(user, token):
#             user.profile.email_confirmed = True
#             user.save()
#             login(request, user)
#             return redirect('index')
#         else:
#             # invalid link
#             return render(request, 'registration/invalid.html')
