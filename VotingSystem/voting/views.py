from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Candidate, Voter

@login_required
def vote(request):
    voter, created = Voter.objects.get_or_create(user=request.user)
    if voter.has_voted:
        return render(request, 'voting/already_voted.html')

    candidates = Candidate.objects.all()
    if request.method == 'POST':
        candidate_id = request.POST.get('candidate')
        candidate = Candidate.objects.get(id=candidate_id)
        candidate.votes += 1
        candidate.save()
        voter.has_voted = True
        voter.save()
        return redirect('vote')
    return render(request, 'voting/vote.html', {'candidates': candidates})

def already_voted(request):
    return render(request, 'voting/already_voted.html')