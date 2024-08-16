from multiprocessing import cpu_count
from os import environ

def max_workers():    
    # return cpu_count() * 2 + 1
    return cpu_count()


bind = '0.0.0.0:' + environ.get('PORT', '8000')
max_requests = 100
workers = max_workers()