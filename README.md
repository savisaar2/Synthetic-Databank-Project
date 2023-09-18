# UniSA Capstone Project: Dataset Generation Application

## Overview

The UniSA Capstone Project is an innovative dataset generation application developed to support research and academic endeavors at the University of South Australia (UniSA). This application provides a streamlined and efficient way to generate custom datasets tailored to specific research needs.

## Installation

To set up this application, follow these simple steps:

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/savisaar2/official-capstone-group-a.git

2. Navigate to the project directory:
    ```bash
    cd unisa_capstone_project

3. Install the required python modules using pip:
    ```bash
    pip install -r requirements.txt

## Top-level directory layout
    .
    ├── controllers             # Contains files for managing the application's logic and handling user interactions.
    ├── datastore               # Houses data related files for the application.
    ├── models                  # Contains files defining data access layer.
    ├── share                   # Share files here related to the project (does not impact on the application).
    ├── tests                   # Contains test files for developer use.
    ├── utils                   # Contains utility files that provide support functions for the application.
    ├── views                   # Contains the frontend 'pages' of the application.
    ├── main.py
    ├── requirements.txt
    └── README.md

## Conventions & Style Guide
    - Indentation: tab (4 spaces) - default in VSCode. 
    - Maximum 120 characters per line. 
    - Class names in Pascal case, appending the architectural desgination e.g. LibraryView, LibraryModel, LibraryController.
    - Class variable / instance variables (methods or attributes) to be in snake_case e.g. self.datasets_collection or self.get_column_headers().
    - Methods of a class that are only to be called by other methods of the same class should be declared semi-private by prefixing the method with an _underscore.
    - Methods of a class that are to be accessible / called from other classes need to be public (no need to prefix with an _underscore).
    - Calling methods / functions intra-extra class or even as nested functions should be done so with keyword arguments to aid in readability and code comprehension.

    > Refer to Documentation on Teams for further conventions.

## Contact

- Alex      - kulay008@mymail.unisa.edu.au
- Htay      - htahy001@mymail.unisa.edu.au
- Hanh      - trahy042@mymail.unisa.edu.au
- Keegan    - walky035@mymail.unisa.edu.au
- Wes       - kenwy002@mymail.unisa.edu.au

