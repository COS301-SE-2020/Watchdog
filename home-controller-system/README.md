# How to run the Home Controller System

1. Install [poetry](https://pypi.org/project/poetrify/). This is used to manage your Python version.

2. Install all dependencies
   ```
   poetry install
   ```
   This will install the current libraries located in the pyproject.lock file. 

# How do I set up my IDE?

Poetry copies your Python interpreter (the one we specified with pyenv) to a special folder, and installs project dependencies into this folder. This is called a Virtual Environment. If there is a `poetry.lock` file then running `poetry install` will install _exactly_ these dependencies, or (if `poetry.lock` is missing) it will install the dependencies from `pyproject.toml` and "lock" them by creating a new `poetry.lock`.

Running `poetry shell` or `poetry run` appends your project's Python interpreter to the front of your `PATH` variable to ensure that you don't use any others. But your IDE must know the path to this Python interpreter if you want it to correctly lint and provide intellisense for your code.

You can get the path pretty easily:

   ```bash
   poetry run which python | pbcopy
   ```

- If you're using **VSCode** you'll need to install the Python extension and provide the above path to the command `> Select Python Interpreter`.
- If you're using **PyCharm**, then specify it under `Preferences > Project: Project Interpreter`. Future versions of [PyCharm may find it automatically](https://youtrack.jetbrains.com/issue/PY-30702).

On a deploy, it doesn't know anything about our dependencies in `pyproject.toml`—it's old school and looks for a `requirements.txt` instead. So we need to make sure that this file exists and contains the same dependencies as `pyproject.toml`:

   ```bash
   poetry run pip freeze > requirements.txt
   ```

OR

we have installed a pyPi library called **poetrify** that is used to pipe the required dependencies to the requirements.txt. All you need to do is run the following command:

   ```bash
   poetry run poetrify generate -d -s requirements.txt
   ```

If you change dependencies, you'll need to remember to generate this file.