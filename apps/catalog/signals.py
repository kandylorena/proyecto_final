from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.management import call_command


@receiver(post_migrate)
def auto_seed(sender, **kwargs):
    if sender.name == 'apps.catalog':
        try:
            from django.apps import apps
            Product = apps.get_model('catalog', 'Product')
            User = apps.get_model('auth', 'User')
            if not Product.objects.exists() or not User.objects.filter(username='admin').exists():
                call_command('seed_data')
        except Exception:
            pass
