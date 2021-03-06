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
        G.add_node(account.public_key, group=account.get_group(), name=str(account))
    for payment in Payment.objects.all():
        G.add_edge(payment.from_account.public_key, payment.to_account.public_key)
    graph_data = json_graph.node_link_data(G)

    return JsonResponse(graph_data)


class StellarAccountDetailView(UpdateView):
    model = StellarAccount
    fields = ["suspect", "kosher", "notes"]
    template_name = "scanner/account.html"


def suspects(request):
    suspect_accounts = set()
    for account in StellarAccount.objects.filter(suspect=True):
        suspect_accounts.add(account.public_key)
        for payment in account.received_payments.all():
            mule = payment.from_account
            if not mule.kosher:
                suspect_accounts.add(mule.public_key)

    output = {"records": list(suspect_accounts)}
    output["count"] = len(suspect_accounts)

    return JsonResponse(output)
