# /etc/mailman3/gunicorn.conf
#
bind = ['127.0.0.1:@WEBPORT@']
proc_name = "mailman-web"
chdir = "@VARDIR@"
pidfile = "@RUNDIR@/gunicorn.pid"
accesslog = "@LOGDIR@/access.log"
errorlog = "@LOGDIR@/error.log"

# Logformat replacing REMOTE_IP by X-Forwarded-For as behind reverse proxy
access_log_format = '%({X-Forwarded-For}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
