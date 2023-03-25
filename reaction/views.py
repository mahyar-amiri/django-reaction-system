from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from reaction.models import React, Reaction, UserReaction


class ReactionView(View, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        urlhash = request.GET.get('urlhash')
        reaction = Reaction.objects.get(urlhash=urlhash)
        user_react = UserReaction.objects.get(user=request.user, reaction__urlhash=urlhash).react if request.user.is_authenticated and UserReaction.objects.filter(user=request.user, reaction__urlhash=urlhash).exists() else None
        reacts = {react: reaction.reactions.filter(react=react).count() for react in reaction.settings.react_emoji.all()}

        context = {
            'reaction': reaction,
            'user_react': user_react,
            'reacts': reacts
        }
        return render(request, 'reaction/reaction.html', context=context)

    def post(self, request, *args, **kwargs):
        user = request.user
        reaction_urlhash = request.POST.get('urlhash', None)
        react_slug = request.POST.get('react_slug', None)

        reaction = UserReaction.objects.filter(user=user, reaction__urlhash=reaction_urlhash).first()

        if reaction:  # Update Previous Reaction
            if reaction.react.slug == react_slug:  # Delete Previous Reaction
                reaction.delete()
            else:  # Change Previous Reaction
                react = React.objects.get(slug=react_slug)
                reaction.react = react
                reaction.save()
        else:  # Create New Reaction
            reaction = Reaction.objects.get(urlhash=reaction_urlhash)
            react = React.objects.get(slug=react_slug)
            UserReaction.objects.create(user=user, reaction=reaction, react=react)

        return HttpResponse(status=200)
