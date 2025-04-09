### Steps to add new kernel

1. cd into the environment folder you wish to add as a kernal in this repo
2. run the following to activate virtual env / or create a new one with `uv sync`
```
source .venv/bin/activate
```

3. run `python -m ipykernel install --name <folder / environment name>` to create the kernel

4. go to jupyter lab web console to locate the new kernal

### Common UV commands

1. `uv sync` to sync the environment with the pyproject.toml prescription
2. `source .venv/bin/activate` to enter the environment
3. `uv pip list` to show all installed packages
