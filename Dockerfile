FROM plus3it/tardigrade-ci:0.0.15

WORKDIR /ci-harness
ENTRYPOINT ["make"]
