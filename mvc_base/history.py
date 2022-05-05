class History:
    """Class for operation history browsing"""

    def __init__(self):
        self.history_list = []
        self.pointer = -1
        self.track = False

    def append(self, history_element):
        """Appends history_element to history_list (if History.track is set to True)"""
        if self.track:
            return
        self.history_list.append(history_element)
        self.pointer += 1

    def pop(self):
        """Removes last history_element from history_list (if History.track is set to True)"""
        if self.track:
            return
        self.history_list.pop()
        self.pointer -= 1

    def decrement(self):
        self.pointer = max(self.pointer - 1, 0)

    def increment(self):
        self.pointer = min(self.pointer + 1, len(self.history_list) - 1)

    def get_tree(self):
        try:
            return self.history_list[self.pointer].controller.tree
        except AttributeError:
            return None

    def get_elem(self):
        if self.pointer >= 0:
            return self.history_list[self.pointer]
        else:
            return None

    def get_prev(self):
        if self.pointer > 0:
            return self.history_list[self.pointer - 1]
        else:
            return None

    def substitute(self, sub):
        self.history_list[self.pointer].tree = sub

    def clear(self):
        self.history_list = []
        self.pointer = -1
        self.track = False


class HistoryElement:
    """Element of history_list"""

    def __init__(self, controller, func, arg):
        # Storing only tree here (instead of controller) causes problems when browsing history
        self.controller = controller
        self.func = func
        self.arg = arg
