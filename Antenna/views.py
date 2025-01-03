import os  
import sys
# Add the parent directory to the sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from django.shortcuts import redirect
from django.contrib import messages
from django.shortcuts import render 
from django.http import HttpResponse
from utils import CustomLogger
from src.Auth import authentication


# ## Create a logger object
# custom_logger = CustomLogger.CustomLogger()
# logger = custom_logger.get_logger()


# Create your views here.
def home(request):
    try:
        #logger.info("Home page accessed")
        return render(request, 'index.html')
    except Exception as e:
        #logger.error(f"Error in home page: {e}")
        return HttpResponse("Error in home page")

## Create a login view
def user_view(request):
    """
    Handles user view requests.

    This view function checks if the user is authenticated. If authenticated, it renders the 'Antenna.html' template.
    Otherwise, it renders the 'login.html' template. In case of an exception, it returns an error message.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered template or an error message.
    """
    try:
        if request.user.is_authenticated:
            return render(request, 'Antenna.html')
        else:
            #logger.info("Login page accessed")
            return render(request, 'login.html')
    except Exception as e:
        #logger.error(f"Error in login page: {e}")
        return HttpResponse("Error in login page")

## Create a signup view   
def signup_view(request):
    """
    Handles signup view requests.

    This view function renders the 'signup.html' template. In case of an exception, it returns an error message.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered template or an error message.
    """
    try:
        auth=authentication()
        
        if request.method == 'POST':
            user_details = {
                'username': request.POST.get('signupusername'),
                'password': request.POST.get('signuppassword'),
                'email': request.POST.get('signupemail'),
                'confirm_password': request.POST.get('signupConfirmpassword')
            }
            
            if not all(user_details.values()):
                messages.error(request, 'Please fill all the fields')
                return redirect("user")
            
            if len(user_details['username']) > 40:
                messages.error(request, 'Username is too long')
                return redirect("user")
            
            if user_details['password'] != user_details['confirm_password']:
                messages.error(request, 'Passwords do not match')
                
                return redirect("user")
            
            response = auth.signup_user(user_details)
            
            if isinstance(response, str):
                messages.error(request, response)
                return redirect("user")
            
            messages.success(request, 'User created successfully')
            return HttpResponse('User created successfully')
        
        
        #logger.info("Signup page accessed")
        return render(request, 'signup.html')
    except Exception as e:
        #logger.error(f"Error in signup page: {e}")
        return HttpResponse("Error in signup page")   
    
## Create a login view    
def user_login(request):
    try:
        auth=authentication()
        
        if request.method == 'POST':
            user_credentials = {
                'username': request.POST.get('Username_login'),
                'password': request.POST.get('Passward_login')
            }
            
            if not all(user_credentials.values()):
                return redirect("user")
            
            response = auth.login_user(request, user_credentials)
            
            if isinstance(response, str):
                messages.error(request, response)
                return redirect("user")
            
            return render('Antenna.html')
        
        #logger.info("Login page accessed")
        return redirect("user")
    except Exception as e:
        #logger.error(f"Error in login page: {e}")
        return HttpResponse("Error in login page")
    
## Create a logout view    
def user_logout(request):
    try:
        auth=authentication()
        auth.logout_user(request)
        #logger.info("User logged out")
        return redirect("index")
    except Exception as e:
        #logger.error(f"Error in logout: {e}")
        return HttpResponse("Error in logout")    