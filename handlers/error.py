from mainhandler import Handler
class CommentError(Handler):
    def get(self):
        self.write('Error')
