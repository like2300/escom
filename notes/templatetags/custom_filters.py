from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Récupère une valeur d'un dictionnaire par clé"""
    return dictionary.get(key, '')



register = template.Library()

@register.filter
def multiply(value, arg):
    """
    Multiplie la valeur par l'argument
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def percentage(value, total):
    """
    Calcule le pourcentage
    """
    try:
        if total == 0:
            return 0
        return (float(value) / float(total)) * 100
    except (ValueError, TypeError):
        return 0

@register.filter
def divide(value, arg):
    """
    Divise la valeur par l'argument
    """
    try:
        if float(arg) == 0:
            return 0
        return float(value) / float(arg)
    except (ValueError, TypeError):
        return 0