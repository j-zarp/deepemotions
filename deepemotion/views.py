# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.templatetags.static import static
from django.http import HttpResponse
import json

# Create your views here.

from core import effect
import urllib
import re
from collections import OrderedDict
    
def IndexView(request):
    prob=[0,0,0,0,0,0]
    emotions = OrderedDict()
    emotions['Joie']=['happy', '#ff9900', '#ffff99']
    emotions['Colère']=['angry', '#ff0000', '#800000']
    emotions['Tristesse']=['sad', '#0033cc', '#0099cc']
    emotions['Peur']=['scared', '#006600', '#009900']
    emotions['Surprise']=['surprised', '#3366cc', '#66ffff']
    emotions['Neutre']=['neutral', '#669999', '#99ccff']
    if request.is_ajax():
        URL=request.POST.get("url")
        screen=request.POST.get("img")
        url=urllib.urlopen(URL)
        with open('static/temp.jpeg', 'wb') as f:
            f.write(url.read())
        prob,label=effect.transform('static/temp.jpeg')
        prob=[str(x) for x in prob]
        screen=screen.replace("/static/","/home/jeremie/jeremie/topten/static/")
        screen=re.sub('<script.*?</script>',"",screen)
        screen=re.sub('<div id="camera".*?<\/div>.*?<\/div>.*?<\/div>','<div id="results" style="float:left;margin-top:125px;">	    <img id="t_pic2" src="/home/jeremie/jeremie/topten/static/temp.jpeg">	    </div>',screen)
        f=open("static/out.html","w")
        f.write(screen.encode('utf-8'))
        f.close()
        return HttpResponse(json.dumps({"prob":prob,"label":label}),content_type="application/json")
    return render(request, 'deepemotion/index.html',{"emotions":emotions})
