class Controller:
    def __init__(self, model, view):
        self.view = view
        self.model = model

    def start(self):
        self.view.start_mainloop()