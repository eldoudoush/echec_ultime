import pygame

class EventHandler:
    def __init__(self):
        self.lst = []
        self.init_lst()

    def init_lst(self):
        for i in range(20):
            self.lst.append([])

    def activer_event(self,event,arg=None):
        if event >= len(self.lst) :
            print("event ",event,"n'est pas initialiser")
            return
        for elem in self.lst[event]:
            if not callable(elem):
                continue
            if arg is None :
                elem()
            else :
                elem(arg)

    def enlever_event(self,event,func):
        if func in self.lst[event] :
            self.lst[event].remove(func)

    def ajouter_event(self,event,func):
        self.lst[event].append(func)

eventhandler = EventHandler()