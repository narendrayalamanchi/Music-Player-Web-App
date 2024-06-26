from django.shortcuts import render,redirect
from .models import Users
from .forms import SignupForm,LoginForm

# Create your views here.
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
            if users.exists:
                return redirect('home')
            else:
                response["message"] = "Invalid Credentials/No User Found"
                response["success"] = False
    else:
        form = LoginForm
        response["form"] = form

    return render(request,'authentication/login.html', response)