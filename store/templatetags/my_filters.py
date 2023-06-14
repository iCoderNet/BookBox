from django import template

register = template.Library()

@register.filter
def check_url_admin(url):
    return 'admin' in url

@register.filter
def check_url_shop(url):
    return 'admin' in url
