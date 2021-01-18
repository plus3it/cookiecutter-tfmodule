FROM plus3it/tardigrade-ci:0.8.1

RUN python -m pip install --no-cache-dir \
  GitPython \
  hub \
  python_terraform

WORKDIR /ci-harness
ENTRYPOINT ["make"]
