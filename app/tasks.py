from django_celery_beat.models import PeriodicTask, IntervalSchedule

# executes every 10 seconds.
schedule, created = IntervalSchedule.objects.get_or_create(
    every=1,
    period=IntervalSchedule.SECONDS,
)

PeriodicTask.objects.create(
    interval=schedule,
    name='Test',
    task='app.tasks.test',
)

def test():
    print('test')
