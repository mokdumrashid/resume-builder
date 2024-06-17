from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, JsonResponse, response
from django.views.generic import TemplateView, ListView, CreateView,  UpdateView, DetailView
from portfolio.forms import UserForm, PortfolioForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from portfolio.models import Portfolio
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from .email_utils import send_email_with_attachment
import pdfkit
import webbrowser
import re
from .models import Portfolio

# Create your views here.
class Home(TemplateView):
    template_name = 'portfolio/index.html'

class personal_info(LoginRequiredMixin, CreateView):
    login_url = '/signin/'
    form_class = PortfolioForm
    model = Portfolio
    context_name = "form"
    template_name = 'portfolio/personal_info.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.username = self.request.user
        obj.save()
        return redirect('cv_template')

class UpdatePersonal_info(LoginRequiredMixin, UpdateView):
    login_url = '/signin/'
    form_class = PortfolioForm
    model = Portfolio
    context_name = "form"
    template_name = 'portfolio/personal_info.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.username = self.request.user
        obj.save()
        return redirect('cv_template')

class cv_list(ListView):
    template_name = 'portfolio/cv_list.html'
    model = Portfolio
    context_object_name = 'port'

class test_template(LoginRequiredMixin, ListView):
    login_url = '/signin/'
    model= Portfolio
    template_name = 'portfolio/templates/index_1.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ports'] = Portfolio.objects.get(username__username=self.request.user.username)
        return context

class text_template2(LoginRequiredMixin, TemplateView):
    login_url = '/signin/'
    model = Portfolio
    template_name = 'portfolio/templates/index_2.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ports'] = Portfolio.objects.get(username__username = self.request.user.username)
        return context

class text_template3(LoginRequiredMixin, TemplateView):
    login_url = '/signin/'
    template_name = 'portfolio/templates/index_3.html'
    model = Portfolio

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)   
        context['ports'] = Portfolio.objects.get(username__username = self.request.user.username)
        return context  

class text_template33(TemplateView):
    login_url = '/signin/'
    template_name = 'portfolio/templates/index_33.html'
    model = Portfolio
    user = authenticate(username="mokdumrashid", password="mokdum@13")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)   
        context['ports'] = Portfolio.objects.get(username__username = "mokdumrashid")
        return context  

class text_template4(LoginRequiredMixin, TemplateView):
    login_url = '/signin/'
    model = Portfolio
    template_name = 'portfolio/templates/index_4.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ports'] = Portfolio.objects.get(username__username=self.request.user.username)
        return context

class text_template5(LoginRequiredMixin, TemplateView):
    login_url = '/signin/'
    template_name = "portfolio/templates/index_5.html"
    model = Portfolio
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ports'] = Portfolio.objects.get(username__username = self.request.user.username)
        return context
           

###############################      REGISTER    #################################
def signup_user(request):
    form_name = UserForm()
    if request.method =="POST":
        form_name = UserForm(request.POST)
        if form_name.is_valid():
            form_name.save()
            messages.success(request, "You have registered successfully")
            return redirect('signin')
        else:
            messages.error(request, 'Invalid input') 
            return redirect('signup')
    else:
        context = {'form_name':form_name}
        return render(request, 'portfolio/signup.html', context)

def signin_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('cv_template')
        else:
            messages.info(request, 'Invalid input.. Please try again.')
            return redirect('signin')
    form = AuthenticationForm()
    context = {'form':form}
    return render(request, 'portfolio/signin.html', context)

def logout_user(request):
    logout(request)
    return redirect('signin')

def my_email_with_attachment_view(request):

    my_str=Portfolio.objects.values_list('reference', flat=True).first()
    context = {'form':my_str}
    r_list = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", my_str)

    subject = 'Application for Software Engineer'
    message = 'Assalamu alaikum, You are seeking a talented developers,  I am interested in working for you. I have attached my CV to this email.'
    from_email = 'mokdum.mysoft@gmail.com'  # Replace with your email address
    recipient_list =  r_list # ['mokdumrashid@gmail.com'] Replace with the recipient's email address

    # Attach the file
    # Attach the file from the sibling folder "documents" of the templates folder
    attachment_path = 'mokdum_rashid.pdf'  # Replace with the relative path to the file from the root directory

    file_path = settings.BASE_DIR / attachment_path
    #file_path = attachment_path

    send_email_with_attachment(subject, message, from_email, recipient_list, attachment_path)

    # ... Rest of your view logic ...
    return HttpResponse("Email with your CV Sent Successfully to the reference mail")

def generate_PDF(request):
    path_wkhtmltopdf = 'C:\Program Files\wkhtmltopdf\\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    login_url = '/signin/'
    template_name = 'portfolio/templates/index_33.html'
    model = Portfolio
    user = authenticate(username="mokdumrashid", password="mokdum@13")

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(**kwargs)   
        context['ports'] = Portfolio.objects.get(username__username = "mokdumrashid")
        return context 
    
    pdfkit.from_url('http://localhost:8000/template33/', 'mokdum_rashid.pdf', configuration=config)
    #response = HttpResponse(pdf, content_type='application/pdf') 
    #response['Content-Disposition'] = 'attachment; filename="mokdum-rashid.pdf"'
    
    webbrowser.open_new(r'file://D:\\PGDIT\\resume-builder\\mokdum_rashid.pdf')

    return HttpResponse("Generate Successfully")

    
        

