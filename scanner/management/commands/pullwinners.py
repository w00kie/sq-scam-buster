from time import sleep
import random
from typing import Any, Optional
from stellar_sdk import Server
import requests
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError, CommandParser

from scanner.models import Badge, StellarAccount

# from pprint import pprint


class Command(BaseCommand):
    help = "Pulls all winner accounts of a SQ Badge and start looking for scammers"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("asset_code", type=str, help="Something like SQ0302")

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        try:
            badge: Badge = Badge.objects.get(asset_code=options["asset_code"])
        except Badge.DoesNotExist:
            raise CommandError(f"Couldn't find badge {options['asset_code']}")

        server = Server(random.choice(settings.HORIZON_ENDPOINTS))
        pmt_api = server.payments().for_account(badge.asset_issuer).limit(200).include_failed(False).call()
        # pprint(pmt_api)
        pmts = []
        while len(pmt_api["_embedded"]["records"]) > 0:
            pmts.extend(pmt_api["_embedded"]["records"])
            self.stdout.write(self.style.NOTICE(f"Found {len(pmt_api['_embedded']['records'])} entries."))
            sleep(2)
            pmt_api = requests.get(pmt_api["_links"]["next"]["href"]).json()

        count = 0
        for pmt in pmts:
            if pmt.get("from") != badge.asset_issuer and pmt.get("asset_code") != badge.asset_code:
                continue
            recipient, created = StellarAccount.objects.get_or_create(
                public_key=pmt.get("to"),
            )
            recipient.has_sq_badges = True
            recipient.badges = list(set(recipient.badges + [badge.asset_code]))
            recipient.save()
            count += 1

        self.stdout.write(self.style.SUCCESS(f"Saved {count} recipients in the database."))
