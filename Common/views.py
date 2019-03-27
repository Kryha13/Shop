from django.contrib.auth import login
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from Common.forms import UserRegisterForm


class RegisterView(View):
    template_name = 'register.html'
    form_class = UserRegisterForm

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()
            login(request, user)
            return redirect('/')

        return render(request, self.template_name, {'form': form})