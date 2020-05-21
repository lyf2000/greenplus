from django.shortcuts import render


# Create your views here.


def chat(request):
    return render(request, 'chat/exp.html')


def user(request):
    return render(request, 'chat/user.html')


def page(request):
    # chats = list(request.user.chats.all().values_list('id', flat=True))
    chats = request.user.chats.all()

    context = {
        # 'chats': chats,

    }
    return render(request, 'chat/page.html', context)
