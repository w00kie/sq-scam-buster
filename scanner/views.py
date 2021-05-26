from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import DetailView
import networkx as nx
from networkx.readwrite import json_graph

from .models import StellarAccount, Payment


def home(request):
    return render(request=request, template_name="home.html")


def graph_data(request):
    G = nx.Graph()

    for account in StellarAccount.objects.all():
        G.add_node(account.public_key, has_sq_badges=account.has_sq_badges)
    for payment in Payment.objects.all():
        G.add_edge(payment.from_account.public_key, payment.to_account.public_key)
    graph_data = json_graph.node_link_data(G)

    return JsonResponse(graph_data)


class StellarAccountDetailView(DetailView):
    model = StellarAccount
    template_name = "scanner/account.html"
