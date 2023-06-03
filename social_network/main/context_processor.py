from main.forms import UserRegistrationForm

# This method was registered in the settings.py file in our project: 
# Now we can use our registration form like {{registraion}} wherenever we need:
def get_context_data(request):
    context = {
        'registration': UserRegistrationForm ,
    }
    return context