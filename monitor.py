import sys
import time
import logging
import subprocess

from watchdog.observers import Observer
from watchdog.events import LoggingFileSystemEventHandler

def log(info):
    print('[Monitor] %s' % info)

class my_loggingfilehandler(LoggingFileSystemEventHandler):
    def __init__(self,action):
        super(my_loggingfilehandler, self).__init__()
        self.restart = action
    
    def on_any_event(self,event):
        if event.src_path[-3:] == '.py':
            log('Python source file changed: %s' % event.src_path)
            self.restart()

process = None

def start_process():
    global process
    global app
    log(('Start process %s...' % app))
    process = subprocess.Popen('python '+app)

def kill_process():
    global process
    if process:
        log('Kill process [%s]...' % process.pid)
        process.kill()
        process.wait()
        log('Process ended with code %s.' % process.returncode)
        process = None
    

def restart_process():
    kill_process()
    start_process()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        log('Parameter should be two!\n please enter python dest.py')
        exit(0)
    global app
    app = sys.argv[1]
    event_handler = my_loggingfilehandler(action = restart_process)
    my_observer = Observer()
    my_observer.schedule(event_handler, '.', recursive=True)
    my_observer.start()
    start_process()
    try :
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        my_observer.stop()
    my_observer.join()