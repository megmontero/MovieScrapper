"""
Component for progress information
"""
from os import system, name 
from threading import Thread
import time
import math


class ProgressBar(Thread):

    def __init__(self, total_func, partial_func, mode='text', delay=1,
                 title=''):
        Thread.__init__(self)
        self._total_func = total_func
        self._partial_func = partial_func
        self._mode = mode
        self._delay = delay
        self._title = title
        self._total_width = 100
        if mode=='text':
            self._print_func = self._display_text
        elif mode=='bar':
            self._print_func = self._display_bar
        self._finished = False
        self.start()

    def _clear(self): 
        # for windows 
        if name == 'nt': 
            _ = system('cls') 
      
        # for mac and linux(here, os.name is 'posix') 
        else: 
            _ = system('clear') 

    def _display_text(self, value):
        print('Current progress: {}'.format(value))

    def _display_bar(self, value):
        print('Current progress:')
        completed = math.floor(round(value))
        incompleted = self._total_width - completed
        print('[' + '='*completed + ' '*incompleted + '] {}%'. format(round(value, 2)))

    def run(self):
        while not self._finished:
            # self._clear()
            print(self._title)
            total = self._total_func()
            partial = self._partial_func()
            if total == 0:
                print('Waiting...')
            else:
                percentage_value = (partial / total) * 100
                self._print_func(percentage_value)
                if (percentage_value == 100):
                    self._finished = True
            time.sleep(self._delay)
            