FROM plus3it/tardigrade-ci:0.3.0

WORKDIR /ci-harness
ENTRYPOINT ["make"]
