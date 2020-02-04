FROM plus3it/tardigrade-ci:0.0.6

WORKDIR /ci-harness
ENTRYPOINT ["make"]
