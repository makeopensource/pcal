# pcal
Pcal is an open-source project organization and devleopment package
## Install
1. `git clone` pcal (ssh preferred)
2. in terminal, `cd` into the cloned directory, and type `pip install .`
## Help
Usage: pcal [OPTIONS] COMMAND [ARGS]...

  Program Calendar for Autograder

Options:
* --version  Show the version and exit.
* --help     Show this message and exit.
* -f         Force command (in development)

Commands:
* clear   Used for testing purposes
* init    Initializes a pcal directory
* remove  Removes a project
* setup   Completes Autograder setup
* status  Lists all projects by due date
* submit  Submits a project to Autograder (in development)
