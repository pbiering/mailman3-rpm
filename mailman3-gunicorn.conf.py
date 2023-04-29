# /etc/mailman3/gunicorn.conf
#
bind = ['127.0.0.1:@WEBPORT@']
proc_name = "mailman-web"
chdir = "@VARDIR@"
pidfile = "@RUNDIR@/gunicorn.pid"
accesslog = "@LOGDIR@/access.log"
errorlog = "@LOGDIR@/error.log"

# Logformat add X-Forwarded-For (useful if running behind reverse proxy)
# https://docs.gunicorn.org/en/stable/settings.html
access_log_format = '%(h)s %({X-Forwarded-For}i)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
