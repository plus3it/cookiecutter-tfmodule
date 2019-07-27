provider "github" {}


module "this" {
  source = "git::https://github.com/plus3it/terraform-github-repo.git?ref=0.0.0"

  name                      = "${var.name}"
  enable_strict_checks      = "${var.enable_strict_checks}"
  enforce_admins            = "${var.enforce_admins}"
  enforce_code_owner_review = "${var.enforce_code_owner_review}"
  required_status_checks    = "${var.required_status_checks}"
  enable_issues             = "${var.enable_issues}"
  enable_merge_commits      = "${var.enable_merge_commits}"
  enable_squash_merging     = "${var.enable_squash_merging}"
  enable_rebase_merging     = "${var.enable_rebase_merging}"
  topics                    = "${var.topics}"
  access_teams              = "${var.access_teams}"
  restricted_pr_teams       = "${var.restricted_pr_teams}"
  restricted_push_teams     = "${var.restricted_push_teams}"
}
