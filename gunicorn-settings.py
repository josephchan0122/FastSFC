""" Gunicorn WSGI server configuration."""
from multiprocessing import cpu_count
import os

def max_workers():
  return cpu_count()

# bind = '100.79.40.104:' + environ.get('PORT', '3002')
bind = os.getenv('IP', '127.0.0.1:3002')

max_requests = 1000
workers = max_workers()
