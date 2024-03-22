from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.urls import reverse
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import University, AboutUs , SocialMediaLinks
from .forms import AboutUsForm

# Mixin for permission check
class AdminRequiredMixin(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            return redirect(reverse('login'))  # Redirect to login if user is not admin
        return super().dispatch(request, *args, **kwargs)

class AboutUsDetailView(View):
    def get(self, request, *args, **kwargs):
        university = get_object_or_404(University, pk=kwargs['university_id'])
        about_us = get_object_or_404(AboutUs, university=university)
        context = {
            'university': university,
            'about_us': about_us,
        }
        return render(request, 'about_us_detail.html', context)

class AboutUsUpdateView(LoginRequiredMixin, UpdateView):
    model = AboutUs
    form_class = AboutUsForm
    template_name = 'about_us_form.html'
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.university.user != self.request.user:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

class AboutUsCreateView(LoginRequiredMixin, CreateView):
    model = AboutUs
    form_class = AboutUsForm
    template_name = 'about_us_form.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.university = University.objects.get(pk=self.kwargs['university_id'])
        return super().form_valid(form)
    def index(request):
        return HttpResponse("Hello, world. You're at the index.")

class AboutUsDeleteView(LoginRequiredMixin, DeleteView):
    model = AboutUs
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.university.user != self.request.user:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

class AboutUsMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['university'] = University.objects.get(pk=self.kwargs['university_id'])
        return context
    
   