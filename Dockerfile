FROM plus3it/tardigrade-ci:0.24.9

RUN pyenv global $(make python38/version) && pyenv rehash && python --version

RUN python -m pip install --no-cache-dir \
  GitPython \
  hub \
  python_terraform

WORKDIR /ci-harness
ENTRYPOINT ["make"]
