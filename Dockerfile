FROM plus3it/tardigrade-ci:0.3.1

WORKDIR /ci-harness
ENTRYPOINT ["make"]
