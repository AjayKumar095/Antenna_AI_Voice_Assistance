import os  
import sys
# Add the parent directory to the sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from django.shortcuts import render 
from django.http import HttpResponse
from utils import CustomLogger


## Create a logger object
custom_logger = CustomLogger.CustomLogger()
logger = custom_logger.get_logger()


# Create your views here.
def home(request):
    try:
        #logger.info("Home page accessed")
        return render(request, 'index.html')
    except Exception as e:
        #logger.error(f"Error in home page: {e}")
        return HttpResponse("Error in home page")

