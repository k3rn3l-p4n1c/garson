import sys
from bot.register import Registerer
from bot.scraper import credit
from userpanel.models import UserCollection
from bot.daemon import Daemon
import datetime
from time import sleep

__author__ = 'bardia'

RESERVE_START_TIME = datetime.time(0, 30, 0)


class MyDaemon(Daemon):
    def run(self):
        global user
        log_file = open('bot/logs/' + str(datetime.datetime.now().date()), "a")
        log_file.write("INF -\t Started at " + str(datetime.datetime.now().time()) + '\n')
        now = datetime.datetime.now()
        # Day of week Monday = 0, Sunday = 6
        day_to_start = (8 - now.weekday()) % 7
        sleep_time = datetime.timedelta(days=day_to_start,
                                        hours=RESERVE_START_TIME.hour - now.hour,
                                        minutes=RESERVE_START_TIME.minute - now.minute,
                                        seconds=RESERVE_START_TIME.second - now.second)
        log_file.write(
            "INF -\t " + str(sleep_time) + " to start! Sleeping " + str(sleep_time.total_seconds()) + " seconds...\n")
        sleep(sleep_time.total_seconds())

        start_time = datetime.datetime.now()
        log_file.write("INF -\t I'm awake!! " + str(start_time) + '\n')
        for user in UserCollection.objects():
            log_file.write("INF -\t Register: " + str(user.stu_username) + '\n')
            res = Registerer(user).register()
            if res is not None:
                log_file.write("ERR -\t ERROR:\n " + res + '\n')
            user.credit = credit(user.stu_username, user.stu_password)
        end_time = datetime.datetime.now()
        log_file.write("INF -\t Process time: " + str(end_time - start_time) + '\n')

        for i in range(7):
            sleep(24 * 60 * 60)
            log_file.write("INF -\t Updating credit " + str(datetime.datetime.now()) + '\n')
            for user in UserCollection.objects():
                user.credit = credit(user.stu_username, user.stu_password)
            user.save()
            log_file.write("INF -\t End of updating credit " + str(datetime.datetime.now()) + '\n')


if __name__ == "__main__":
    daemon = MyDaemon('/tmp/daemon-garson.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)