FROM plus3it/tardigrade-ci:0.0.12

WORKDIR /ci-harness
ENTRYPOINT ["make"]
