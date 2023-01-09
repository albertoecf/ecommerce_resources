
from . models import CategoryClass
def menu_links(request):
    links = CategoryClass.objects.all()
    return dict(links=links)
