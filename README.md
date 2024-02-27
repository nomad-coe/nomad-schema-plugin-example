![](https://github.com/nomad-coe/nomad-schema-plugin-example/actions/workflows/actions.yml/badge.svg)
![](https://coveralls.io/repos/github/FAIRmat-NFDI/nomad-analysis/badge.svg?branch=main)

# NOMAD's Analysis plugin
This is a plugin for [NOMAD](https://nomad-lab.eu) to facilitate analysis of processed entry archives using Jupyter notebooks.

## Getting started


### Install the dependencies

You should create a virtual environment. You will need the `nomad-lab` package (and `pytest`).
You need Python 3.9.

```sh
python3.9 -m venv .pyenv
source .pyenv/bin/activate
pip install --upgrade pip
pip install '.[dev]' --index-url https://gitlab.mpcdf.mpg.de/api/v4/projects/2187/packages/pypi/simple
```

**Note!**
Until we have an official pypi NOMAD release with the plugins functionality. Make
sure to include NOMAD's internal package registry (e.g. via `--index-url`).


### Run the tests

Make sure the `src` directory is in your path:

```sh
export PYTHONPATH=./src
```

You can run automated tests with `pytest`:

```sh
pytest -svx tests
```

## Development

The plugin is still under development. If you would like to contribute, install the package in editable mode with the development dependencies:

```sh
pip install -e .[dev] --index-url https://gitlab.mpcdf.mpg.de/api/v4/projects/2187/packages/pypi/simple
```

### Setting up plugin on your local installation
Read the [NOMAD plugin documentation](https://nomad-lab.eu/prod/v1/staging/docs/howto/oasis/plugins_install.html) for all details on how to deploy the plugin on your NOMAD instance.

You need to modify the ```nomad.yaml``` configuration file of your NOMAD instance.
To include the analysis plugin you need to add the following lines: .

```yaml
plugins:
  include:
  - 'schemas/nomad_analysis'
  options:
    schemas/nomad_analysis:
      python_package: nomad_analysis
```

You also need to add the `src` folder to the `PYTHONPATH` of the Python environment of your local NOMAD installation. With this, `nomad_analysis` package can be found by Python. Either run the following every time you start a new terminal for running the appworker, or add it to your virtual environment in `{path to local NOMAD installation}/.pyenv/bin/activate` file: 

```sh
export PYTHONPATH="$PYTHONPATH:{path to the root of nomad-analysis repo}/src"
```

### Run linting

```sh
ruff check .
```

### Run auto-formatting

This is entirely optional. To add this as a check in github actions pipeline, uncomment the `ruff-formatting` step in `./github/workflows/actions.yaml`.

```sh
ruff format .
```

## Next steps

To learn more about plugins, how to add them to an Oasis, how to publish them, read our
documentation: https://nomad-lab.eu/docs/.
