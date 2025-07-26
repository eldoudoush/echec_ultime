import pygame

class EventHandler:
    def __init__(self):
        self.lst = []

    def init_dic(self):
        for i in range(20):
            self.lst.append([])

    def activer_event(self,event):
        if event >= len(self.lst) :
            print("event ",event,"n'est pas initialiser")
            return
        for elem in self.lst[event]:
            if callable(elem):
                elem()

    def ajouter_event(self,event,func):
        self.dic[event].append(func)

eventhandler = EventHandler()