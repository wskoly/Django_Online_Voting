from django.shortcuts import render

def index(request):
    return render(request,'index.html')
def vote(request):
    return render(request,'muni_election/vote.html')
def standings(request):
    return render(request,'muni_election/standings.html')
