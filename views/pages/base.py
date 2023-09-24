from customtkinter import CTkLabel, CTkCanvas, CTkFrame

class BaseView(CTkFrame):
    def __init__(self, root, title_text, description_text, *args, **kwargs):
        """
        Initialise the Base view class of the application.
        It will be used by each new page to extend upon.

        Parameters
        ----------
        title_text : str
            A summative title for the page.
        description_text : str
            A short description of the page.
        """
        # Send parameters to CTkFrame.
        super().__init__(root.view_frame, fg_color="transparent", *args, **kwargs)

        # Display our title.
        self._render_title(title_text, description_text)

        self.place(
            relx=0.5, rely=0.5, anchor="center",
            relwidth=1, relheight=1
        )

    def _render_title(self, title_text, description_text):
        """
        Renders the title section of CTkFrame.

        Parameters
        ----------
        title_text : str
            A summative title for the page.
        description_text : str
            A short description of the page.
        """
        # Main title for the page.
        title = CTkLabel(self, text=title_text, font=("Arial", 21, "bold"), anchor="w")
        title.pack(padx=20, pady=(20, 0), fill="both")

        # Short description for the page.
        desc = CTkLabel(self, text=description_text, font=("Arial", 16), anchor="w")
        desc.pack(padx=20, pady=(0, 0), fill="both")

        # Draw a line to separate the title section from the body.
        line = CTkCanvas(self, height=1, bg="gray", highlightthickness=0)
        line.pack(pady=20, fill="both")
        line.create_line(0, 0, self.winfo_width(), 0)