from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
from apps.sports.forms import UpdateFootballMatch
from apps.sports.models import FootballMatch, FootballBookmaker


def boldtv_index(request):
    all_match = FootballMatch.objects.all().order_by('-id')
    page = request.GET.get('page', 1)

    paginator = Paginator(all_match, 10)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
    context = {'segment':'boldtv_index','data':data}
    html_template = loader.get_template('sports/bolddktv.html')
    return HttpResponse(html_template.render(context, request))

def edit(request, id):
    data = FootballMatch.objects.get(id=id)
    bookmakers = FootballBookmaker.objects.filter(match_id=id)
    # return HttpResponse()
    context = {'segment': 'boldtv_index', 'data': data, 'bookmakers':bookmakers,'range':range(3-bookmakers.count())}
    return render(request, 'sports/bolddktv_update.html', context)

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

def update(request,id):
    data = FootballMatch.objects.get(id=id)
    if 'channel_logo' in request.FILES and len(request.FILES['channel_logo']) != 0:
        data.channel_img = request.FILES['channel_logo']
        file_type = data.channel_img.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in IMAGE_FILE_TYPES:
            data.channel_img = None
    # return HttpResponse(request.POST.items())
    # bookmakers
    if 'bookmaker[1][default]' in request.POST:
        url = 'https://spilexpert.dk/comparison/go/ticker/unibet-sport-dk'
        img = 'bookmakers/DK_Unibet_Sport_logo_130_40_1614731035.png'
        match_id = id
        FootballBookmaker.objects.create(url=url, match_id=match_id, img=img)
    elif 'bookmaker[1][logo]' in request.FILES and len(request.FILES['bookmaker[1][logo]']) != 0:
        url = request.POST['bookmaker[1][url]']
        match_id = id
        img = request.FILES['bookmaker[1][logo]']
        bookmaker_1 = FootballBookmaker.objects.create(url=url, match_id=match_id, img=img)
        bookmaker_1.img = request.FILES['bookmaker[1][logo]']
        file_type = bookmaker_1.img.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in IMAGE_FILE_TYPES:
            bookmaker_1.img = None
        bookmaker_1.save()
    if 'bookmaker[2][default]' in request.POST:
        url = 'https://spilexpert.dk/comparison/go/ticker/mr-green-sport-dk'
        img = 'bookmakers/DK_Mr_Green_Sport_logo_130_40_1614887005.png'
        match_id = id
        FootballBookmaker.objects.create(url=url, match_id=match_id, img=img)
    elif 'bookmaker[2][logo]' in request.FILES and len(request.FILES['bookmaker[2][logo]']) != 0:
        url = request.POST['bookmaker[2][url]']
        match_id = id
        img = request.FILES['bookmaker[2][logo]']
        bookmaker_2 = FootballBookmaker.objects.create(url=url, match_id=match_id, img=img)
        bookmaker_2.img = request.FILES['bookmaker[2][logo]']
        file_type = bookmaker_2.img.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in IMAGE_FILE_TYPES:
            bookmaker_2.img = None
        bookmaker_2.save()
    if 'bookmaker[3][default]' in request.POST:
        url = 'https://spilexpert.dk/comparison/go/ticker/comeon-sport-dk'
        img = 'bookmakers/DK_Comeon_Sport_logo_130_40_1617348760.png'
        match_id = id
        FootballBookmaker.objects.create(url=url, match_id=match_id, img=img)
    elif 'bookmaker[3][logo]' in request.FILES and len(request.FILES['bookmaker[3][logo]']) != 0:
        url = request.POST['bookmaker[3][url]']
        match_id = id
        img = request.FILES['bookmaker[3][logo]']
        bookmaker_3 = FootballBookmaker.objects.create(url=url, match_id=match_id, img=img)
        bookmaker_3.img = request.FILES['bookmaker[3][logo]']
        file_type = bookmaker_3.img.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in IMAGE_FILE_TYPES:
            bookmaker_3.img = None
        bookmaker_3.save()
    data.save()
    return HttpResponseRedirect('/boldtv')