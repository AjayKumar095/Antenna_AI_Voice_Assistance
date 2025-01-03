## 0. Importing the necessary modules
import os 
import sys 
import django
## Add the path to the sys.path list
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

## Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Antenna.settings")
django.setup()

## 1. Importing the necessary modules
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.models import User
from utils.CustomLogger import customLogger
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import  check_password
from datetime import datetime

## 2. Create a class called authentication
class authentication():
    """
    This class handles user authentication.

    The `login_user` method logs in the authenticated user.
    The `logout_user` method logs out the user.
    The `signup_user` method creates a new user account.
    """

    @staticmethod
    def login_user(request, user_credentials:dict):
        """
        Logs in the authenticated user.

        Args:
            request (HttpRequest): The HTTP request object.
            user (User): The authenticated user object.
        """
        try:
            if user_credentials:
               
               try:
                     user=User.objects.get(username=user_credentials['username'])
               except User.DoesNotExist:
                    return "User does not exist"   
                
               if check_password(user_credentials['password'],user.password):
                    user=authenticate(request,username=user_credentials['username'],password=user_credentials['password'])
                    if user is not None:
                        login(request,user)
                        return user
                    else:
                        return "Invalid credentials"  
            else:
                return "User credentials not provided"
         
        except Exception as e:
            return "Error while logging in, Please try again later."

    @staticmethod
    def logout_user(request):
        """
        Logs out the user.

        Args:
            request (HttpRequest): The HTTP request object.
        """
        logout(request)
    
    @staticmethod
    def signup_user(User_details:dict):
        """
        Registers a new user with the provided details.
        Args:
            user_details (dict): A dictionary containing user information required for signup.
        Returns:
            None
        """
        try:
           if User_details:
               if User.objects.filter(username=User_details['username']).exists():
                   return "User already exists"
               else:
                   if User_details['password']==User_details['confirm_password']:
                       validate_password(User_details['password'])
                       user=User.objects.create_user(username=User_details['username'],
                                                     email=User_details['email'],
                                                     password=User_details['password'],
                                                     date_joined=datetime.now())
                       user.save()
                       return user
                   else :
                        return "Passwords do not match"
           else :
                return "User details not provided"
        
        except ValidationError as e:
            return e.messages[0]
         
        except Exception as e:
            return "Error while creating user, Please try again later."


    