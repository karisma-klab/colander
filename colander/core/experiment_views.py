from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib import messages
from django_q.tasks import async_task

from colander.core.forms import CommentForm
from colander.core.models import PiRogueExperiment, Artifact
from colander.core.pcap_tasks import save_decrypted_traffic
from colander.core.views import get_active_case, CaseRequiredMixin


class PiRogueExperimentCreateView(LoginRequiredMixin, CaseRequiredMixin, CreateView):
    model = PiRogueExperiment
    template_name = 'pages/collect/experiments.html'
    success_url = reverse_lazy('collect_experiment_create_view')
    fields = [
        'name',
        'pcap',
        'socket_trace',
        'sslkeylog',
        'screencast',
        'tlp',
        'pap'
    ]

    def get_form(self, form_class=None):
        active_case = get_active_case(self.request)
        artifacts_qset = Artifact.get_user_artifacts(self.request.user, active_case)
        form = super(PiRogueExperimentCreateView, self).get_form(form_class)
        form.fields['pcap'].queryset = artifacts_qset.filter(type__short_name='PCAP')
        form.fields['socket_trace'].queryset = artifacts_qset.filter(type__short_name='SOCKET_T')
        form.fields['sslkeylog'].queryset = artifacts_qset.filter(type__short_name='SSLKEYLOG')
        form.fields['screencast'].queryset = artifacts_qset.filter(type__short_name='VIDEO')
        return form

    def form_valid(self, form):
        active_case = get_active_case(self.request)
        if form.is_valid() and active_case:
            device = form.save(commit=False)
            device.owner = self.request.user
            device.case = active_case
            device.save()
            form.save_m2m()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['experiments'] = PiRogueExperiment.get_user_pirogue_dumps(self.request.user,
                                                                      self.request.session.get('active_case'))
        ctx['is_editing'] = False
        return ctx


class PiRogueExperimentUpdateView(PiRogueExperimentCreateView, UpdateView):
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['experiments'] = PiRogueExperiment.get_user_pirogue_dumps(self.request.user,
                                                                      self.request.session.get('active_case'))
        ctx['is_editing'] = True
        return ctx


class PiRogueExperimentDetailsView(LoginRequiredMixin, CaseRequiredMixin, DetailView):
    model = PiRogueExperiment
    template_name = 'pages/collect/experiment_details.html'
    context_object_name = 'experiment'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['comment_form'] = CommentForm()
        return ctx


@login_required
def start_decryption(request, pk):
    if PiRogueExperiment.objects.filter(id=pk).exists():
        experiment = PiRogueExperiment.objects.get(id=pk)
        if experiment.pcap and experiment.sslkeylog:
            messages.success(request, 'Traffic decryption is in progress, refresh this page in a few minutes.')
            async_task(save_decrypted_traffic, pk)
        else:
            messages.error(request, 'Cannot decrypt traffic since your experiment does not have both a PCAP file and an SSL keylog file.')
    return redirect(request.META.get('HTTP_REFERER'))
