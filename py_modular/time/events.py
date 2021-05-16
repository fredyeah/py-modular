import random

class Event:
    """
    :param nodes: An array of nodes that should have events triggered
    :type nodes: array
    """
    def __init__(self, nodes=None):
        self.nodes = nodes
    def event_callback(self, node, time):
        """
        :param node: A node for which an event should be called
        :param time: A value of time in seconds
        :type time: float
        """
        pass
    def get_event(self, time):
        """
        :param time: A value of time in seconds
        :type time: float
        """
        for node in self.nodes:
            self.event_callback(node, time)

class PitchEvent(Event):
    def event_callback(self, node, time):
        node.freq = (random.random() * 100 + 120)

class TriggerEvent(Event):
    def event_callback(self, node, time):
        node.trigger(time)
