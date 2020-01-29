FROM plus3it/tardigrade-ci:0.0.5

WORKDIR /ci-harness
ENTRYPOINT ["make"]
