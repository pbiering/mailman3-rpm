# /etc/mailman3/gunicorn.conf
#
bind = ['127.0.0.1:@WEBPORT@']
proc_name = "mailman-web"
chdir = "@VARDIR@"
pidfile = "@RUNDIR@/gunicorn.pid"
accesslog = "@LOGDIR@/access.log"
errorlog = "@LOGDIR@/error.log"
