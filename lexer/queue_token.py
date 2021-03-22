class QueueToken:
    def __init__(self):
        self.queue = []

    def append_token(self, token):
        self.queue.append(token)

    def get_queue(self):
        return self.queue