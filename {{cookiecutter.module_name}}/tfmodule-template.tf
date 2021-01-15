# Simple module declaration for dependency management via dependabot

module "github-repo" {
  source = "git::https://github.com/plus3it/terraform-github-repo.git?ref=2.0.0"
}
