class ExceptionController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.frame = self.view.frames["exception"]
        self._bind()

    def _bind(self):
        self.frame.info_button.configure(command=lambda: self._hide_info())
        self.frame.error_button.configure(command=lambda: self._hide_error())

    def _hide_error(self):
        self.frame.hide_error_view()

    def _hide_info(self):
        self.frame.hide_info_view()