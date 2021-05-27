from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic.edit import UpdateView
from django.db.models import Count, Q
import networkx as nx
from networkx.readwrite import json_graph

from .models import StellarAccount, Payment


def home(request):
    return render(request=request, template_name="home.html")


def graph_data(request):
    G = nx.Graph()

    for account in StellarAccount.objects.annotate(
        num_issued=Count("issued_payments"),
        num_received=Count("received_payments"),
    ).filter(Q(num_issued__gt=0) | Q(num_received__gt=0)):
        if account.has_sq_badges:
            group = "quester"
        elif account.directory_tags:
            group = account.directory_tags[0]
        elif account.suspect:
            group = "suspect"
        else:
            group = "unknown"
        G.add_node(account.public_key, group=group)
    for payment in Payment.objects.all():
        G.add_edge(payment.from_account.public_key, payment.to_account.public_key)
    graph_data = json_graph.node_link_data(G)

    return JsonResponse(graph_data)


class StellarAccountDetailView(UpdateView):
    model = StellarAccount
    fields = ["suspect", "notes"]
    template_name = "scanner/account.html"
