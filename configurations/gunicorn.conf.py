# DO NOT RUN from COMMAND LINE
# systemctl usage: ExecStart=/home/maste/.local/bin/gunicorn
# kill using kill $(cat PID_FILE)
import multiprocessing
import app

workers = multiprocessing.cpu_count() * 2 + 1
threads = 2
bind = ['unix:gunicorn.sock']
preload_app = True
pidfile = 'gunicorn.pid'
daemon = False
wsgi_app = 'app:app'
capture_output = True
errorlog = 'gunicorn.log'
umask = 0o007

on_starting = app.on_starting
on_exit = app.on_exit
