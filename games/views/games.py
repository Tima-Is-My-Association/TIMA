from app.functions.piwik import track
from app.functions.score import calculate_points
from app.models import Profile
from association.functions.words import get_next_word, get_next_word_by_association
from association.models import Association, Language, Word
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_protect
from games.forms import AssociationChainForm
from games.models import AssociationChain

def games(request):
    track(request, 'Games | TIMA')
    return render(request, 'tima/games/game/games.html', locals())

@csrf_protect
@login_required(login_url='/signin/')
def associationchain(request, slug=None):
    track(request, 'AssociationChain | Games | TIMA')
    if slug:
        language = get_object_or_404(Language, slug=slug)

        if request.method == 'POST':
            form = AssociationChainForm(request.POST)
            if form.is_valid():
                if not request.user.is_anonymous():
                    language.users.add(get_object_or_404(Profile, user=request.user))
                    language.save()

                chain = AssociationChain.objects.get(id=form.cleaned_data['chain_id'])
                if form.cleaned_data['word'] == form.cleaned_data['association']:
                    word = Word.objects.get(name=form.cleaned_data['word'], language=language)
                    return render(request, 'games/associationchain/game.html', locals())

                word = get_object_or_404(Word, name=form.cleaned_data['word'], language=language)
                word1, created = Word.objects.get_or_create(name=form.cleaned_data['association'], language=language)

                if AssociationChain.objects.filter(chain_id=chain.id).filter(word=word).exists():
                    messages.add_message(request, messages.ERROR, _('You lost.'))
                    won = False
                    chains = AssociationChain.objects.filter(chain_id=chain.chain_id)
                    return render(request, 'tima/games/associationchain/end.html', locals())

                association, created = Association.objects.update_or_create(word=word, association=word1)
                points = calculate_points(request.user, association)
                messages.add_message(request, messages.INFO, _('You received %(points)s points for your association of %(association)s.') % {'points': points, 'association': association})

                chain = AssociationChain.objects.create(user=request.user, word=word1, previous=chain, chain_id=chain.chain_id)
                word = get_next_word_by_association(word1, association_chain=chain)
                if word:
                    chain = AssociationChain.objects.create(user=request.user, word=word, previous=chain, chain_id=chain.chain_id)
                    association1 = ''
                    form = AssociationChainForm(initial={'word':word.name, 'language':language.code, 'chain_id':chain.id})
                    return render(request, 'tima/games/associationchain/game.html', locals())
                else:
                    messages.add_message(request, messages.SUCCESS, _('You won.'))
                    won = True
                    chains = AssociationChain.objects.filter(chain_id=chain.chain_id)
                    return render(request, 'tima/games/associationchain/end.html', locals())
            else:
                word = Word.objects.get(name=form.cleaned_data['word'], language=language)
                association1 = form.cleaned_data['association1']
                return render(request, 'tima/games/associationchain/game.html', locals())
        else:
            AssociationChain.objects.filter(user=request.user).delete()
            word = get_next_word(language=language, user=request.user)
            chain = AssociationChain.objects.create(user=request.user, word=word)
            association1 = ''
            form = AssociationChainForm(initial={'word':word.name, 'language':language.code, 'chain_id':chain.id})
            return render(request, 'tima/games/associationchain/game.html', locals())
    else:
        AssociationChain.objects.filter(user=request.user).delete()
        languages = Language.objects.all()
        return render(request, 'tima/games/associationchain/home.html', locals())
