FROM plus3it/tardigrade-ci:0.2.0

WORKDIR /ci-harness
ENTRYPOINT ["make"]
