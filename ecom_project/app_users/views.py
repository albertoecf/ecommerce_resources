from django.shortcuts import render
from .models import UserClass

# Create your views here.
def users_list_views(request):
    users_all = UserClass.objects.all()

    users_dic = {
        'users_all' : users_all
    }

    return render(request, 'users_list.html', users_dic)
