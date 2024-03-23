from .models import Category


def categories(request):
    """
    A function that retrieves categories with no parent from the database.
    """
    return {'categories': Category.objects.filter(parent=None)}