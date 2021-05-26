import random
from tqdm import tqdm
import maya
from time import sleep
from typing import Any, Optional
from stellar_sdk import Server, Network, TransactionEnvelope, Payment as PaymentOperation
from django.conf import settings
from django.core.management.base import BaseCommand

from scanner.models import Payment, StellarAccount

# from pprint import pprint


class Command(BaseCommand):
    help = "Pulls the last 50 payments out of accounts in database."

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        progress_bar = tqdm(desc="Processing", total=StellarAccount.objects.filter(has_sq_badges=True).count())

        for account in StellarAccount.objects.filter(has_sq_badges=True):
            server = Server(random.choice(settings.HORIZON_ENDPOINTS))
            tx_api = server.transactions().for_account(account.public_key).limit(50).include_failed(False).call()
            # pprint(tx_api)
            records = tx_api["_embedded"]["records"]

            for record in records:
                try:
                    memo = record.get("memo", "")
                    transaction_hash = record.get("hash")
                    created_at = maya.MayaDT.from_iso8601(record.get("created_at"))
                    source = record.get("source_account")

                    try:
                        tx = TransactionEnvelope.from_xdr(
                            record.get("envelope_xdr"), Network.PUBLIC_NETWORK_PASSPHRASE
                        )
                    except ValueError:
                        # Probably a FeeBump from the SQ badge account
                        continue

                    for op in tx.transaction.operations:
                        # Take source from op if defined, else transaction source
                        source = op.source if op.source else source

                        if not isinstance(op, PaymentOperation):
                            continue
                        if source != account.public_key:
                            continue

                        amount = f"{op.amount} {op.asset.code}"

                        destination, created = StellarAccount.objects.get_or_create(
                            public_key=op.destination,
                        )
                        if created:
                            destination.save()

                        payment, created = Payment.objects.get_or_create(
                            transaction_hash=transaction_hash,
                            defaults={
                                "from_account": account,
                                "to_account": destination,
                                "amount": amount,
                                "memo": memo,
                                "created_at": created_at.datetime(),
                            },
                        )
                        if created:
                            payment.save()
                except Exception as e:
                    tqdm.write(self.style.WARNING(f"Encountered an error: {e}"))

            progress_bar.update(1)
            sleep(1)

        progress_bar.close()
        self.stdout.write(self.style.SUCCESS(f"Saved {10} recipients in the database."))
