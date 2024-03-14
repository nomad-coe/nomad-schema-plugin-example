FROM gitlab-registry.mpcdf.mpg.de/nomad-lab/nomad-fair:latest

RUN pip install build

COPY \
    src/nomad_analysis \
    tests \
    README.md \
    LICENSE \
    pyproject.toml \
    .

RUN python -m build --sdist

RUN pip install dist/nomad-analysis-*.tar.gz
