from .celery import app as celery_app

# Expose the Celery app under the name `celery` so that callers which do
# `-A ecomm` (or import ecomm and look for `ecomm.celery`) find the
# application object. This keeps compatibility with common Celery/Django
# conventions.
celery = celery_app

__all__ = ['celery_app', 'celery']