#!/bin/sh

#CF20130116 this is based on http://heyheymymy.net/django/deploying-django-project-with-nginx-and-uwsgi-in-ubuntu-10-04
# and /etc/init.d/uwsgi is a symlink to it.

PATH=/sbin:/bin:/usr/sbin:/usr/bin
DAEMON=/usr/local/bin/uwsgi #/path/to/foo/bin/uwsgi
OWNER=uwsgi
NAME=uwsgi
DESC=uwsgi
#make isaute2 accessible
PYTHONPATH=/home/fisk/virt/justfruitcake/fruitcakesite    #/path/to/foo
#virtual python env home
HOME=/home/fisk/virt/justfruitcake #/path/to/foo
MODULE=/home/fisk/virt/justfruitcake/fruitcakesite/fruitcakesite/wsgi.py #project.wsgi
 
test -x $DAEMON || exit 0
 
# Include uwsgi defaults if available
if [ -f /etc/default/uwsgi ] ; then
        . /etc/default/uwsgi
fi
         
set -e
         
DAEMON_OPTS="-s 127.0.0.1:9001 -M 4 -t 30 -A 4 -p 4 -d /var/log/uwsgi.log --pythonpath $PYTHONPATH --module $MODULE --home $HOME"
         
case "$1" in
    start)
        echo -n "Starting $DESC: "
        start-stop-daemon --start --chuid $OWNER:$OWNER --user $OWNER \
            --exec $DAEMON -- $DAEMON_OPTS
        echo "$NAME."
        ;;
    stop)
        echo -n "Stopping $DESC: "
        start-stop-daemon --signal 3 --user $OWNER --quiet --retry 2 --stop \
            --exec $DAEMON
        echo "$NAME."
        ;;
    reload)
        killall -1 $DAEMON
        ;;
    force-reload)
        killall -15 $DAEMON
        ;;
    restart)
        echo -n "Restarting $DESC: "
        start-stop-daemon --signal 3 --user $OWNER --quiet --retry 2 --stop \
            --exec $DAEMON
        sleep 1
        start-stop-daemon --user $OWNER --start --quiet --chuid $OWNER:$OWNER \
            --exec $DAEMON -- $DAEMON_OPTS
        echo "$NAME."
        ;;
    status)  
        killall -10 $DAEMON
        ;;
      *)  
            N=/etc/init.d/$NAME
            echo "Usage: $N {start|stop|restart|reload|force-reload|status}" >&2
            exit 1
            ;;
      esac
    exit 0

