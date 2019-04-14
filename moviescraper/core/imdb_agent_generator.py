"""
IMDBAgentGenerator
"""

import random


class IMDBAgentGenerator():

    class UserAgentGenerator():
        def __init__(self):
            self._user_agent_list = [('Mozilla/5.0 (Windows NT 6.1; WOW64) Ap'
                                      'pleWebKit/537.36 (KHTML, like Gecko) Ch'
                                      'rome/54.0.2840.99 Safari/537.36'),
                                     ('Mozilla/5.0 (Windows NT 10.0; WOW64) Ap'
                                      'pleWebKit/537.36 (KHTML, like Gecko) Ch'
                                      'rome/54.0.2840.99 Safari/537.36'),
                                     ('Mozilla/5.0 (Windows NT 10.0; Win64; x6'
                                      '4) AppleWebKit/537.36 (KHTML, like Geck'
                                      'o) Chrome/54.0.2840.99 Safari/537.36'),
                                     ('Mozilla/5.0 (Macintosh; Intel Mac OS X '
                                      '10_12_1) AppleWebKit/602.2.14 (KHTML, l'
                                      'ike Gecko) Version/10.0.1 Safari/602.2.'
                                      '14'),
                                     ('Mozilla/5.0 (Windows NT 10.0; WOW64) Ap'
                                      'pleWebKit/537.36 (KHTML, like Gecko) Ch'
                                      'rome/54.0.2840.71 Safari/537.36'),
                                     ('Mozilla/5.0 (Macintosh; Intel Mac OS X '
                                      '10_12_1) AppleWebKit/537.36 (KHTML, lik'
                                      'e Gecko) Chrome/54.0.2840.98 Safari/537'
                                      '.36'),
                                     ('Mozilla/5.0 (Macintosh; Intel Mac OS X '
                                      '10_11_6) AppleWebKit/537.36 (KHTML, lik'
                                      'e Gecko) Chrome/54.0.2840.98 Safari/537'
                                      '.36'),
                                     ('Mozilla/5.0 (Windows NT 6.1; WOW64) App'
                                      'leWebKit/537.36 (KHTML, like Gecko) Chr'
                                      'ome/54.0.2840.71 Safari/537.36'),
                                     ('Mozilla/5.0 (Windows NT 6.1; Win64; x64'
                                      ') AppleWebKit/537.36 (KHTML, like Gecko'
                                      ') Chrome/54.0.2840.99 Safari/537.36'),
                                     ('Mozilla/5.0 (Windows NT 10.0; WOW64; rv'
                                      ':50.0) Gecko/20100101 Firefox/50.0')]
            self._num_agents = len(self._user_agent_list) - 1

        def random(self):
            return self._user_agent_list[random.randint(0, self._num_agents)]

    def __init__(self):
        self._generator = self.UserAgentGenerator()

    def random_agent(self):
        return self._generator.random()
