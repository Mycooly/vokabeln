from django import template


# Filter zum Formatieren in den HTML-Dateien

def percentage(value):
    return '{0:.2%}'.format(value)


register = template.Library()

register.filter('percentage', percentage)
