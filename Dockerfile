FROM plus3it/tardigrade-ci:0.0.11

WORKDIR /ci-harness
ENTRYPOINT ["make"]
