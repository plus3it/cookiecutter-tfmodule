"""Create GitHub project."""

import os
import json
import re
import shutil
import subprocess
import tempfile

import git

from python_terraform import Terraform

# get the github url of tfmodule template
TF_GITHUB_REPO_SOURCE = "tfmodule-template.tf"

with open(TF_GITHUB_REPO_SOURCE) as tf:
    tf_file = tf.read()
TF_MODULE_URL = re.search('source = "(.*)"', tf_file).group(1)

# remove the template file to avoid it getting added to the new repo
os.remove(TF_GITHUB_REPO_SOURCE)

YES_OPTIONS, NO_OPTIONS = frozenset(["y", "yes"]), frozenset(["n", "no", ""])
PERM_OPTIONS = frozenset(["push", "pull", "admin"])


def multiple_choices(question):
    """Return multiple choice user selection."""
    selection = []
    additional = "Would you like to add another (y/n)? [n]: "

    check = True
    while check:
        choice = input(question).lower()
        selection.append(choice)
        check = check_choice(additional)
    return selection


def check_choice(question):
    """Return valid user yes/no answer."""
    while True:
        choice = input(question).lower()
        if choice in YES_OPTIONS:
            return True
        if choice in NO_OPTIONS:
            return False


def get_collaborators():
    """Return list of collaborators to add to the project."""
    collaborators = []
    collab_q = "Grant an organizational team access to the repo(y/n)? [n]: "

    if check_choice(collab_q):
        add_team = True

        while add_team:
            teams_q = "What team would you like to grant access? "
            team = input(teams_q).lower()

            if team != "":
                perm = None
                while perm not in PERM_OPTIONS:
                    perms_q = (
                        "What permissions would you like to grant them"
                        " (push, pull, admin)? "
                    )
                    perm = input(perms_q).lower()
                collaborators.append({"name": team, "permission": perm})

            another_q = "Would you like to add another team (y/n)? [n]: "
            add_team = check_choice(another_q)

    return collaborators


def run_terraform(directory, terraform_vars, target_module):
    """Run terraform init and apply."""
    terraform = Terraform(directory)
    terraform.init(from_module=target_module)

    with open(directory + "terraform.tfvars.json", "w") as fh_:
        fh_.write(json.dumps(terraform_vars))

    # ret_code, stdout, stderr
    _, _, _ = terraform.apply(
        auto_approve=True, capture_output=False, raise_on_error=True
    )


def open_pr(source_repo, working_dir):
    """Open a pull request."""
    # create a temp dir
    temp_dir = tempfile.mkdtemp()

    # clone the repo
    git.Repo.clone_from(source_repo, temp_dir)

    # Move the cloned contents up a directory
    # because we can't clone to an existing directory
    for file_name in os.listdir(temp_dir):
        shutil.move(
            os.path.join(working_dir, temp_dir, file_name),
            os.path.join(working_dir, file_name),
        )
    os.rmdir(temp_dir)

    # init the repo obj
    repo = git.Repo(working_dir)

    # create a new branch
    new_branch = repo.create_head("init")

    # checkout the new branch
    new_branch.checkout()

    # add all files in working dir to a new commit in the newly created branch
    repo.git.add("--all")
    repo.git.commit(m="Module initialization")

    # push the changes
    repo.git.push("--set-upstream", "origin", new_branch)

    # open a PR
    subprocess.check_call(["hub", "pull-request", "--no-edit"])


def main():
    """Create GitHub project."""
    if "{{ cookiecutter.create_repo }}".lower() == "yes":
        subprocess.check_call(["git", "init"])
        subprocess.check_call(["hub", "create"])
    elif "{{ cookiecutter.create_org_repo }}".lower() == "yes":
        print("\nPost hook questions\n")
        # Yes/No Questions
        yn_questions = {
            "enable_strict_checks": "Require branches to be up to"
            + " date before merging (y/n)? [n]: ",
            "enforce_admins": "Require admins to oblige by status checks (y/n)? [n]: ",
            "enforce_code_owner_review": "Require a designated code owner to"
            + " approve pull requests (y/n)? [n]: ",
            "enable_issues": "Enable the GitHub Issues features"
            + " on the repository (y/n)? [n]: ",
            "enable_merge_commits": "Allow merge commits (y/n)? [n]: ",
            "enable_squash_merging": "Allow squash merging (y/n)? [n]: ",
            "enable_rebase_merging": "Allow rebase merging (y/n)? [n]: ",
        }

        # Multiple entry questions
        dict_questions = {
            "topics": {
                "start_question": "Add a topic to the repository (y/n)? [n]: ",
                "init_loop": "What topic would you like to add? ",
            },
            "required_status_checks": {
                "start_question": "Add required checks for merging into"
                + " the branch (y/n)? [n]: ",
                "init_loop": "What check would you like to add? ",
            },
            "restricted_pr_teams": {
                "start_question": "Restrict which teams can dismiss push requests"
                + " (y/n)? [n]: ",
                "init_loop": "What team would you like to restrict? ",
            },
            "restricted_push_teams": {
                "start_question": "Restrict who can push to the branch (y/n)? [n]: ",
                "init_loop": "What team would you like to restrict? ",
            },
        }

        directory = "terraform/"
        os.mkdir(directory)
        token_q = (
            "Enter the personal access token for creating the organizational repo: "
        )
        os.environ["GITHUB_ORGANIZATION"] = "{{ cookiecutter.github_username }}"
        os.environ["GITHUB_TOKEN"] = input(token_q).lower()

        terraform_vars = {
            "name": "{{ cookiecutter.module_name }}",
            "description": "{{ cookiecutter.short_description }}",
        }

        for var, question in yn_questions.items():
            choice = check_choice(question)
            terraform_vars[var] = str(choice).lower()

        for var, question in dict_questions.items():
            choice = check_choice(question["start_question"])
            if choice:
                selection = multiple_choices(question["init_loop"])
                terraform_vars[var] = selection

        collaborators = get_collaborators()
        if collaborators:
            terraform_vars["access_teams"] = collaborators

        run_terraform(directory, terraform_vars, TF_MODULE_URL)

        shutil.rmtree(os.path.join(os.getcwd(), directory))
        source_repo = (
            "https://github.com/"
            "{{ cookiecutter.github_username }}/"
            "{{ cookiecutter.module_name }}.git"
        )
        open_pr(source_repo, os.getcwd())


if __name__ == "__main__":
    main()
