from url_shortener.celery import app
from url_shortener.models import ShortenedURL


@app.task(name='tasks.update_num_visits', ignore_result=True)
def update_num_visits(short_code):
    """
    Asynchronous task to increase the number of visits
    """
    try:
        shortened_url = ShortenedURL.objects.get(short_code=short_code)
    except ShortenedURL.DoesNotExist:
        return
    shortened_url.num_visits += 1
    shortened_url.save()

