from .root import Root

class View:
    def __init__(self):
        self.root = Root()
        self.frames = {}

    def _add_frame(self, view_class, name):
        self.frames[name] = view_class(self.root)

    def switch_view(self, name):
        self.current_view = self.frames[name]
        self.current_view.lift()

    def start_mainloop(self):
        self.root.mainloop()