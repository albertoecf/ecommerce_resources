from django.shortcuts import render

# Create your views here.
def users_list_views(request):
    return render(request, 'users_list.html')
