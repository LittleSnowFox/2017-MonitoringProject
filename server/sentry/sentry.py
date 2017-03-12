import requests
from server.monitoring.models import WebSite
import datetime
from celery import Celery
from server.run import db

celery = Celery()
celery.conf.broker_url = 'redis://redis:6379/0'
celery.conf.result_backend = 'redis://redis:6379/0'


@celery.on_after_configure.connect
def register_celery_scheduler(sender, **kwargs):
    sender.add_periodic_task(10.0, celery_monitoring, name='monitor')


def monitor(url):
    """
    This function is doing the monitoring.

    It will query the url specified in parameter and return a tuple
    indicating if the site is online, the status code and the response time

    In case the site is down we will return False, -1, -1

    :param url: url to query
    :type url: string
    :return A tuple like (is online?, status code, time)
    :rtype Tuple
    """
    try:
        answer = requests.get(url)
        return True, answer.status_code, answer.elapsed.total_seconds()
    except requests.exceptions.Timeout:
        return False, -1, -1


@celery.task
def celery_monitoring():
    """

    :return:
    """

    # FIXME : debug to delete
    # try:
    #    f_debug = open("/tmp/debug.log", "r+")
    # except Exception as e:
    #    f_debug = open("/tmp/debug.log", "w+")

    # We get the site that we need to monitor
    list_websites = WebSite.query.filter(WebSite.last_time_monitored <= datetime.datetime.now()).all()
    for website in list_websites:
        answer = monitor(website.url)

        if answer[0]:
            print("server is online and answered in {}".format(answer[2]))
            if answer[1] >= 400:
                print(" but site is down")
            else:
                print(" and site is up")
        else:
            print("server is down it didn't answer to our request")
        website.last_time_monitored = datetime.datetime.now()
        db.session.commit()
        # FIXME : debug to delete
    #    f_debug.write(str(website) + " " + str(answer))
    # f_debug.close()
    return 1
