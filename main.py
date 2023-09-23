from models.main import Model
from views.main import View
from controllers.main import Controller

def main():
    """
    Entry point for the application.

    This function initialises the core components of the application, including the Model,
    View, and Controller. It then begins the application by calling the Controller's start method.
    """
    # Initialise the core MVC components of the application
    model = Model()
    view = View()
    controller = Controller(model, view)

    # Start the application
    controller.start()

if __name__ == "__main__":
    main()