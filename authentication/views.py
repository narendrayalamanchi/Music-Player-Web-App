from django.shortcuts import render,redirect
from .models import Users
from .forms import SignupForm,LoginForm
from django.contrib.auth import logout
from music_dashboard.models import Song

# Create your views here.
def index(request):
    return render(request,'music_dashboard/index.html')

def signout(request):
    logout(request)
    return render(request,'music_dashboard/index.html')
                  
def signup(request):
    response = {"success":True}
    if request.method == 'POST':
        form = SignupForm(request.POST)
        print("POST",request.POST)
        if form.is_valid():
            print("Inside SAVE")
            form.save()
            return redirect('login')
        else:
            response["message"] = "Invalid Details. (Username should atleast 2 and maximum of 8 characters)"
            response["success"] = False
    else:
        form = SignupForm()
        response["form"] = form

    return render(request,'authentication/register.html', response)

def login(request):
    response = {"success":True}
    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            users = Users.objects.filter(email=email, password = password)
            if users.exists():
                request.session["is_logged"] = True
                request.session["username"] = users[0].username
                return redirect('home')
            else:
                response["message"] = "Invalid Credentials/No User Found"
                response["success"] = False
    else:
        form = LoginForm
        response["form"] = form

    return render(request,'authentication/login.html', response)

def home(request):
    res = Song.objects.all()
    return render(request,'music_dashboard/home.html',{"result":res})