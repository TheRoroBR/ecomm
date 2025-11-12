from django.core.management.base import BaseCommand

from shop.models import Product


class Command(BaseCommand):
    help = 'Set all Product.stock values to 999 (destructive).'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help='Show what would be changed without saving.')

    def handle(self, *args, **options):
        dry_run = options.get('dry_run', False)
        qs = Product.objects.all()
        total = qs.count()
        self.stdout.write(f'Found {total} products.')
        if dry_run:
            # Show a simple distribution of current stock values
            try:
                from django.db.models import Count

                dist = qs.values('stock').annotate(c=Count('id')).order_by('-c')
                for row in dist:
                    self.stdout.write(f"stock={row['stock']}: {row['c']} products")
            except Exception:
                # If aggregation fails for any reason, just list first few products
                for p in qs[:10]:
                    self.stdout.write(f"id={p.id} stock={p.stock}")
            self.stdout.write('Dry run enabled; no changes made.')
            return

        updated = qs.update(stock=999)
        self.stdout.write(self.style.SUCCESS(f'Successfully updated {updated} products to stock=999.'))
