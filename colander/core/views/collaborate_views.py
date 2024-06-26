from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from colander.core.forms import AddRemoveTeamContributorForm
from colander.core.models import ColanderTeam
from colander.core.views.views import OwnershipRequiredMixin
from colander.users.models import User


class ColanderTeamCreateView(LoginRequiredMixin, CreateView):
    model = ColanderTeam
    template_name = 'pages/collaborate/teams.html'
    success_url = reverse_lazy('collaborate_team_create_view')
    fields = [
        'name',
    ]
    case_required_message_action = "create teams"

    def get_form(self, form_class=None):
        form = super(ColanderTeamCreateView, self).get_form(form_class)
        return form

    def form_valid(self, form):
        if form.is_valid():
            team = form.save(commit=False)
            if not hasattr(team, 'owner'):
                team.owner = self.request.user
            team.save()
            form.save_m2m()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['teams'] = ColanderTeam.get_user_teams(self.request.user)
        ctx['is_editing'] = False
        return ctx


class ColanderTeamUpdateView(ColanderTeamCreateView, OwnershipRequiredMixin, UpdateView):
    case_required_message_action = "update team"
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['teams'] = ColanderTeam.get_user_teams(self.request.user)
        ctx['is_editing'] = True
        return ctx


class ColanderTeamDetailsView(LoginRequiredMixin, OwnershipRequiredMixin, DetailView):
    model = ColanderTeam
    template_name = 'pages/collaborate/team_details.html'
    context_object_name = 'team'
    case_required_message_action = "view team details"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = AddRemoveTeamContributorForm()
        return ctx


@login_required
def add_remove_team_contributor(request, pk):
    team = ColanderTeam.objects.get(id=pk)
    if team.owner != request.user:  # Todo: support team administrators
        return HttpResponseForbidden()
    if request.method == 'POST' and team.owner == request.user:
        form = AddRemoveTeamContributorForm(request.POST)
        if form.is_valid():
            contributor_id = form.cleaned_data['contributor_id']
            if contributor_id == request.user.contributor_id and 'add_contributor' in request.POST:
                messages.warning(request, 'You can not add the owner of this team as a contributor too.')
            else:
                try:
                    contributor = User.objects.get(contributor_id=contributor_id)
                    if 'add_contributor' in request.POST \
                        and contributor is not team.owner \
                        and contributor not in team.contributors.all():
                        team.contributors.add(contributor)
                        team.save()
                        messages.success(request, f'{contributor} has been added to the team {team.name}.')
                    if 'remove_contributor' in request.POST \
                        and contributor is not team.owner \
                        and contributor in team.contributors.all():
                        team.contributors.remove(contributor)
                        team.save()
                        messages.success(request, f'{contributor} has been removed from the team {team.name}.')
                except User.DoesNotExist:
                    messages.error(request, f'Contributor {contributor_id} does not exist.')
    return redirect("collaborate_team_details_view", pk=team.id)


@login_required
def delete_team_view(request, pk):
    team = ColanderTeam.objects.get(id=pk)
    if team.owner == request.user:
        team.delete()
    else:
        return HttpResponseForbidden()
    return redirect("collaborate_team_create_view")
