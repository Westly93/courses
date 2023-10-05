from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View


from .forms import (
    CustomPasswordChangeForm,
    ProfileUpdateForm,
    UserRegisterForm,
    UserUpdateForm,
)
from .models import Profile, UserAccount


class UserRegisterView(View):
    def get(self, request, *args, **kwargs):
        form = UserRegisterForm()
        return render(request, "accounts/register.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Your Account has been created successifully, You can now login!",
            )
            return redirect("accounts:login")
        return render(request, "accounts/register.html", {"form": form})


class UserProfileView(LoginRequiredMixin, View):
    # login_url = '/login/'
    def test_func(self):
        # Define the test function to check if the user is a guest
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        # Redirect the user if they fail the test
        login_url = reverse(
            "accounts:login"
        )  # Replace 'login' with the URL or name of the login page
        next_url = (
            self.request.get_full_path()
        )  # Get the current URL as the 'next' parameter
        redirect_url = (
            # Append 'next' parameter to the login URL
            f"{login_url}?next={next_url}"
        )
        return redirect(redirect_url)

    def get(self, request, *args, **kwargs):
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        context = {"u_form": u_form, "p_form": p_form}
        return render(request, "accounts/profile.html", context)

    def post(self, request, *args, **kwargs):
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        context = {"u_form": u_form, "p_form": p_form}
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(
                request, "You profile has been updated successfully!")
            return redirect("accounts:dashboard")
        messages.warning(request, "Failed to update your profile!")
        return render(request, "accounts/profile.html", context)


@login_required
def dashboard(request):
    
    return render(request, "accounts/dashboard.html")


class NewPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = "accounts/password_change.html"
    success_url = reverse_lazy(
        "accounts:password_change_done"
    )  # URL to redirect after successful password change


def password_change_done(request):
    return render(
        request, "accounts/password_change_done.html", {
            "title": "password change done"}
    )
