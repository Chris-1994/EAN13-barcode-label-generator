ps aux |grep gunicorn |grep localhost:8007 | awk '{ print $2 }' |xargs kill -HUP
