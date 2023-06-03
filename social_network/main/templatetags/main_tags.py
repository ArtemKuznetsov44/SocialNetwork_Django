from django import template
from django.urls import reverse
from main.models import * 

# New object which can registrate our tags:
register = template.Library()

# Register our tag for burger content creating:
@register.inclusion_tag("main/burger_content.html")
def get_burger_content():

    links = {
        'My Profile': reverse('start_page'),
        'News' : "#" ,
        'Friends': "#",
        'Communities' : "#",
        'Photos' : "#",
        'Music' : "#",
        'Videos' : "#",
        'Stickers' : "#",
        'Market' : "#",
        'Sign out' : "#",  
    }

    return {"links" : links}