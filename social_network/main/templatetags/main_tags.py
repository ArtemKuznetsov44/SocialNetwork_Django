from django import template
from django.urls import reverse
from main.models import *

# New object which can registrate our tags:
register = template.Library()

links = {
    'My Profile': reverse('start_page'),
    'News': "#",
    'Friends': reverse('friends_page'),
    'Communities': "#",
    'Photos': "#",
    'Music': "#",
    'Videos': "#",
    'Stickers': "#",
    'Market': "#",
    'Sign out': reverse('sign_out'),
}

# Register our tag for burger content creating:
@register.inclusion_tag("main/burger_content.html")
def get_burger_content():
    return {"links": links}

# Register our tag for left menue content creating: 
@register.inclusion_tag("main/left_menue.html")
def get_left_menu():
    return {'links': links}

@register.filter
def get_from_dict(dictionary, key):
    return dictionary.get(key)

@register.filter
def remove_quotes(text):
    return text.replace('"', '')