variable "name" {
  description = "The name of the repostory to create"
  type        = "string"
}

variable "description" {
  description = "Description for the repository being created"
  type        = "string"
}

variable "enable_strict_checks" {
  description = "Require branches to be up to date before merging."
  type        = "string"
  default     = "false"
}

variable "enforce_admins" {
  description = "Enforces status checks on repository administrators"
  type        = "string"
  default     = "true"
}

variable "enforce_code_owner_review" {
  description = "Require an approved review in pull requests including files with a designated code owner"
  type        = "string"
  default     = "false"
}

variable "required_status_checks" {
  description = "The list of status checks to require in order to merge into this branch."
  type        = "list"
  default     = []
}

variable "enable_issues" {
  description = "Enable the GitHub Issues features on the repository"
  type        = "string"
  default     = "true"
}

variable "enable_merge_commits" {
  description = "Whether or not to allow merge commits"
  type        = "string"
  default     = "true"
}

variable "enable_squash_merging" {
  description = "Whether or not to allow squash merging"
  type        = "string"
  default     = "false"
}

variable "enable_rebase_merging" {
  description = "Whether or not to allow rebase merging"
  type        = "string"
  default     = "false"
}

variable "topics" {
  description = "List of topics to apply to the repository"
  type        = "list"
  default     = []
}


variable "access_teams" {
  description = "List of organizational teams who can access the repository"
  type        = "list"
  default     = []
}

variable "restricted_pr_teams" {
  description = "List of organizational teams who can dismiss a pull request"
  type        = "list"
  default     = []
}

variable "restricted_push_teams" {
  description = "List of organizational teams who can push to the branch"
  type        = "list"
  default     = []
}
