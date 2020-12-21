FROM plus3it/tardigrade-ci:0.5.0

RUN python -m pip install --no-cache-dir \
  GitPython \
  hub \
  python_terraform

WORKDIR /ci-harness
ENTRYPOINT ["make"]
