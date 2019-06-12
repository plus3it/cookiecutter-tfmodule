ARCH ?= amd64
OS ?= $(shell uname -s | tr '[:upper:]' '[:lower:'])
CURL ?= curl --fail -sSL
XARGS ?= xargs -I {}
BIN_DIR ?= ${HOME}/bin
TMP ?= /tmp
FIND_EXCLUDES ?= -not \( -name .terraform -prune \) -not \( -name .terragrunt-cache -prune \)

PATH := $(BIN_DIR):${PATH}

MAKEFLAGS += --no-print-directory
SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c

.PHONY: guard/% %/install %/lint

GITHUB_ACCESS_TOKEN ?= {{cookiecutter.github_readonly_token}}
# Macro to return the download url for a github release
# For latest release, use version=latest
# To pin a release, use version=tags/<tag>
# $(call parse_github_download_url,owner,repo,version,asset select query)
parse_github_download_url = $(CURL) https://api.github.com/repos/$(1)/$(2)/releases/$(3)?access_token=$(GITHUB_ACCESS_TOKEN) | jq --raw-output  '.assets[] | select($(4)) | .browser_download_url'

# Macro to download a github binary release
# $(call download_github_release,file,owner,repo,version,asset select query)
download_github_release = $(CURL) -o $(1) $(shell $(call parse_github_download_url,$(2),$(3),$(4),$(5)))

# Macro to download a hashicorp archive release
# $(call download_hashicorp_release,file,app,version)
download_hashicorp_release = $(CURL) -o $(1) https://releases.hashicorp.com/$(2)/$(3)/$(2)_$(3)_$(OS)_$(ARCH).zip

guard/env/%:
	@ _="$(or $($*),$(error Make/environment variable '$*' not present))"

guard/program/%:
	@ which $* > /dev/null || $(MAKE) $*/install

$(BIN_DIR):
	@ echo "[make]: Creating directory '$@'..."
	mkdir -p $@

install/gh-release/%: guard/env/FILENAME guard/env/OWNER guard/env/REPO guard/env/VERSION guard/env/QUERY
install/gh-release/%:
	@ echo "[$@]: Installing $*..."
	$(call download_github_release,$(FILENAME),$(OWNER),$(REPO),$(VERSION),$(QUERY))
	chmod +x $(FILENAME)
	$* --version
	@ echo "[$@]: Completed successfully!"

zip/install:
	@ echo "[$@]: Installing $(@D)..."
	apt-get install zip -y
	@ echo "[$@]: Completed successfully!"

terraform/install: TERRAFORM_VERSION_LATEST := $(CURL) https://checkpoint-api.hashicorp.com/v1/check/terraform | jq -r -M '.current_version' | sed 's/^v//'
terraform/install: TERRAFORM_VERSION ?= $(shell $(TERRAFORM_VERSION_LATEST))
terraform/install: | $(BIN_DIR) guard/program/jq
	@ echo "[$@]: Installing $(@D)..."
	$(call download_hashicorp_release,$(@D).zip,$(@D),$(TERRAFORM_VERSION))
	unzip $(@D).zip && rm -f $(@D).zip && chmod +x $(@D)
	mv $(@D) "$(BIN_DIR)"
	$(@D) --version
	@ echo "[$@]: Completed successfully!"

terraform-docs/install: TFDOCS_VERSION ?= latest
terraform-docs/install: | $(BIN_DIR) guard/program/jq
	@ $(MAKE) install/gh-release/$(@D) FILENAME="$(BIN_DIR)/$(@D)" OWNER=segmentio REPO=$(@D) VERSION=$(TFDOCS_VERSION) QUERY='.name | endswith("$(OS)-$(ARCH)")'

jq/install: JQ_VERSION ?= latest
jq/install: | $(BIN_DIR)
	@ $(MAKE) install/gh-release/$(@D) FILENAME="$(BIN_DIR)/$(@D)" OWNER=stedolan REPO=$(@D) VERSION=$(JQ_VERSION) QUERY='.name | endswith("$(OS)64")'

shellcheck/install: SHELLCHECK_VERSION ?= latest
shellcheck/install: SHELLCHECK_URL ?= https://storage.googleapis.com/shellcheck/shellcheck-${SHELLCHECK_VERSION}.linux.x86_64.tar.xz
shellcheck/install: $(BIN_DIR) guard/program/xz
	$(CURL) $(SHELLCHECK_URL) | tar -xJv
	mv $(@D)-*/$(@D) $(BIN_DIR)
	rm -rf $(@D)-*
	$(@D) --version

terraform/lint: | guard/program/terraform
	@ echo "[$@]: Linting Terraform files..."
	terraform fmt -check=true -diff=true
	@ echo "[$@]: Terraform files PASSED lint test!"

sh/%: FIND_SH := find . $(FIND_EXCLUDES) -name '*.sh' -type f -print0
sh/lint: | guard/program/shellcheck
	@ echo "[$@]: Linting shell scripts..."
	$(FIND_SH) | $(XARGS) shellcheck {}
	@ echo "[$@]: Shell scripts PASSED lint test!"

json/%: FIND_JSON := find . $(FIND_EXCLUDES) -name '*.json' -type f
json/lint: | guard/program/jq
	@ echo "[$@]: Linting JSON files..."
	$(FIND_JSON) | $(XARGS) bash -c 'cmp {} <(jq --indent 4 -S . {}) || (echo "[{}]: Failed JSON Lint Test"; exit 1)'
	@ echo "[$@]: JSON files PASSED lint test!"

json/format: | guard/program/jq
	@ echo "[$@]: Formatting JSON files..."
	$(FIND_JSON) | $(XARGS) bash -c 'echo "$$(jq --indent 4 -S . "{}")" > "{}"'
	@ echo "[$@]: Successfully formatted JSON files!"

docs/%: README_PARTS := _docs/MAIN.md <(echo) <(terraform-docs markdown table .)
docs/%: README_FILE ?= README.md

docs/lint: | guard/program/terraform-docs
	@ echo "[$@]: Linting documentation files.."
	diff $(README_FILE) <(cat $(README_PARTS))
	@ echo "[$@]: Documentation files PASSED lint test!"

docs/generate: | guard/program/terraform-docs
	@ echo "[$@]: Creating documentation files.."
	cat $(README_PARTS) > $(README_FILE)
	@ echo "[$@]: Documentation files creation complete!"
