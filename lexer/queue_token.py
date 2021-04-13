class QueueToken:
    def __init__(self):
        self.queue = []

    def pushLex(self, token):
        self.queue.append(token)

    def get_queue(self):
        return self.queue