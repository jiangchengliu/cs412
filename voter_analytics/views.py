from django.shortcuts import render
from typing import Any
from django.db.models.query import QuerySet
from django.db.models import Q, Count
from django.views.generic import ListView, DetailView
from .models import Voter

# Create your views here.

import plotly.graph_objects as go
import plotly.offline as pyo
from collections import Counter


class ShowAllVoters(ListView):
    model = Voter
    template_name = "voter_analytics/voters.html"
    context_object_name = "voters"
    paginate_by = 100

    def get_queryset(self):
        queryset = Voter.objects.all()

        # Extract search parameters from GET request
        party = self.request.GET.get('party_affiliation')
        min_dob = self.request.GET.get('min_dob')
        max_dob = self.request.GET.get('max_dob')
        voter_score = self.request.GET.get('voter_score')
        v20state = self.request.GET.get('v20state') == 'on'
        v21town = self.request.GET.get('v21town') == 'on'
        v21primary = self.request.GET.get('v21primary') == 'on'
        v22general = self.request.GET.get('v22general') == 'on'
        v23town = self.request.GET.get('v23town') == 'on'

        filter_conditions = Q()

        
        if party:
            filter_conditions &= Q(party_affiliation=party)

        if min_dob:
            filter_conditions &= Q(date_of_birth__gte=f"{min_dob}-01-01")
        if max_dob:
            filter_conditions &= Q(date_of_birth__lte=f"{max_dob}-12-31")

        if voter_score:
            filter_conditions &= Q(voter_score=voter_score)

        if v20state:
            filter_conditions &= Q(v20state=True)
        if v21town:
            filter_conditions &= Q(v21town=True)
        if v21primary:
            filter_conditions &= Q(v21primary=True)
        if v22general:
            filter_conditions &= Q(v22general=True)
        if v23town:
            filter_conditions &= Q(v23town=True)

        queryset = queryset.filter(filter_conditions)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['title'] = 'Voter List View'  
        
        get_copy = self.request.GET.copy()

        if get_copy.get('page'):
            get_copy.pop('page')
        context['get_copy'] = get_copy
        
        return context


class ShowVoter(DetailView):
    model = Voter
    template_name = "voter_analytics/voter_detail.html"
    context_object_name = "voter"


class GraphsView(ListView):
    model = Voter
    template_name = "voter_analytics/graphs.html"
    context_object_name = "voters"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Extract GET parameters from the request
        party = self.request.GET.get('party_affiliation')
        min_dob = self.request.GET.get('min_dob')
        max_dob = self.request.GET.get('max_dob')
        voter_score = self.request.GET.get('voter_score')
        v20state = self.request.GET.get('v20state') == 'on'
        v21town = self.request.GET.get('v21town') == 'on'
        v21primary = self.request.GET.get('v21primary') == 'on'
        v22general = self.request.GET.get('v22general') == 'on'
        v23town = self.request.GET.get('v23town') == 'on'

        # Apply filtering logic
        filter_conditions = Q()

        if party:
            filter_conditions &= Q(party_affiliation=party)
        if min_dob:
            filter_conditions &= Q(date_of_birth__gte=f"{min_dob}-01-01")
        if max_dob:
            filter_conditions &= Q(date_of_birth__lte=f"{max_dob}-12-31")
        if voter_score:
            filter_conditions &= Q(voter_score=voter_score)
        if v20state:
            filter_conditions &= Q(v20state=True)
        if v21town:
            filter_conditions &= Q(v21town=True)
        if v21primary:
            filter_conditions &= Q(v21primary=True)
        if v22general:
            filter_conditions &= Q(v22general=True)
        if v23town:
            filter_conditions &= Q(v23town=True)

        # Apply filters to the queryset
        queryset = Voter.objects.filter(filter_conditions)

        # Add the filtered voters to context
        context['voters'] = queryset

        #Histogram of Voters by Year of Birth
        years_of_birth = queryset.values_list('date_of_birth__year', flat=True)
        year_count = dict(Counter(years_of_birth))  # Use Counter to count occurrences
        years = list(year_count.keys())
        counts = list(year_count.values())

        bar_fig = go.Bar(x=years, y=counts, name="Voters by Year of Birth")
        bar_div = pyo.plot({"data": [bar_fig]}, auto_open=False, output_type="div")
        context['bar_div'] = bar_div

        # Pie chart of Voters by Party Affiliation
        party_count = queryset.values('party_affiliation').annotate(count=Count('party_affiliation'))  # Correct usage of Count
        party_labels = [item['party_affiliation'] for item in party_count]
        party_values = [item['count'] for item in party_count]

        pie_fig = go.Pie(labels=party_labels, values=party_values, name="Voters by Party Affiliation")
        pie_div = pyo.plot({"data": [pie_fig]}, auto_open=False, output_type="div")
        context['pie_div'] = pie_div

        # Histogram of Voters by Election Participation
        elections = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        election_counts = {election: queryset.filter(**{election: True}).count() for election in elections}
        election_labels = [election[1:].capitalize() for election in elections]
        election_values = list(election_counts.values())

        election_bar_fig = go.Bar(x=election_labels, y=election_values, name="Voters by Election Participation")
        election_bar_div = pyo.plot({"data": [election_bar_fig]}, auto_open=False, output_type="div")
        context['election_bar_div'] = election_bar_div

        return context
