import os
import json
import shutil
import subprocess
from python_terraform import *

YES_OPTIONS, NO_OPTIONS = frozenset(["y"]), frozenset(["n", ""])
PERM_OPTIONS = frozenset(["push", "pull", "admin"])

def multiple_choices(question):
    selection = []
    additional = "Would you like to add another (y/n)? "

    while True:
        choice = raw_input(question).lower()
        selection.append(choice)
        if not check_choice(additional):
            break
    return selection

def check_choice(question):
    while True:
        choice = raw_input(question).lower()
        if choice in YES_OPTIONS:
            return True
        if choice in NO_OPTIONS:
            return False

def get_collaborators():
    # Questions that have multiple layers to them
    collaborators = []
    collab_q = "Grant an organizational team access to the repo(y/n)? [n]: "
    collab = check_choice(collab_q)
    if collab:
        while True:
            teams_q = "What team would you like to grant access? "
            team = raw_input(teams_q).lower()

            if team != "":
                while True:
                    perms_q = "What permissions would you like to grant them (push,pull,admin)? "
                    perm = raw_input(perms_q).lower()
                    if perm in PERM_OPTIONS:
                        callaborator = {
                            "name": team,
                            "permission": perm
                        }
                        collaborators.append(callaborator)
                        break

            another_q = "Would you like to add another team (y/n)? [n]: "
            if not check_choice(another_q):
                break

    return collaborators

def run_terraform(directory):
    terraform = Terraform(directory)
    terraform.init()
    ret_code, _, _ = terraform.apply(auto_approve=True, capture_output=False)

    return ret_code

def remove_terraform_files(directory):
    file_names = ["main.tf", "variables.tf", "terraform.tfvars", "terraform.tfstate"]
    for file_name in file_names:
        os.remove(directory +"/"+ file_name)
    shutil.rmtree(directory)

if __name__ == "__main__":
    if "{{ cookiecutter.create_repo }}".lower() == "yes":
        subprocess.check_call(['git', 'init'])
        subprocess.check_call(['hub', 'create'])
    elif "{{ cookiecutter.create_org_repo }}".lower() == "yes":
        # Yes/No Questions
        YN_QUESTIONS = {
            "enable_stict_checks": "Require branches to be up to date before merging (y/n)? [n]: ",
            "enforce_admins": "Require admins to oblige by status checks (y/n)? [n]: ",
            "enforce_code_owner_review": "Require a designated code owner to approve pull requests (y/n)? [n]: ",
            "enable_issues": "Enable the GitHub Issues features on the repository (y/n)? [n]: ",
            "enable_merge_commits": "Allow merge commits (y/n)? [n]: ",
            "enable_squash_merging": "Allow squash merging (y/n)? [n]: ",
            "enable_rebase_merging": "Allow rebase merging (y/n)? [n]: ",
        }

        # Multiple entry questions
        DICT_QUESTIONS = {
            "topics": {
                "start_question": "Add a topic to the repository (y/n)? [n]: ",
                "init_loop": "What topic would you like to add? "
            },
            "required_status_checks": {
                "start_question": "Add required checks for merging into the branch (y/n)? [n]: ",
                "init_loop": "What check would you like to add? "
            },
            "restricted_pr_teams": {
                "start_question": "Restrict which teams can dismiss push requests (y/n)? [n]: ",
                "init_loop": "What team would you like to restrict? "
            },
            "restricted_push_teams": {
                "start_question": "Restrict who can push to the branch (y/n)? [n]: ",
                "init_loop": "What team would you like to restrict? "
            }
        }

        directory = "terraform/"
        token_q = "Enter the personal access token for creating the organizational repo: "
        os.environ['GITHUB_ORGANIZATION'] = "{{ cookiecutter.github_username }}"
        os.environ['GITHUB_TOKEN'] = raw_input(token_q).lower()

        with open( directory  + "/terraform.tfvars", "w") as f:
            f.write("name = " + "\"{{ cookiecutter.module_name }}\"" + "\n")
            f.write("description = " + "\"{{ cookiecutter.short_description }}\"" + "\n")

            for var, question in YN_QUESTIONS.items():
                choice = check_choice(question)
                f.write(var +" = \""+ str(choice).lower() + "\"\n")

            for var, question in DICT_QUESTIONS.items():
                choice = check_choice(question['start_question'])
                if choice:
                    selection = multiple_choices(question['init_loop'])
                    f.write(var +" = "+ json.dumps(selection) + "\n")

            collaborators = get_collaborators()
            if collaborators:
                f.write("access_teams = " + json.dumps(collaborators).replace(":", "=") + "\n")

        success = run_terraform(directory)

        print("Return Code: {}".format(success))
        if success == 0:
            org_repo_script = "org_repo.sh"
            remove_terraform_files(directory)
            bash = subprocess.check_output(["bash", org_repo_script])
            print(bash)
            os.remove(org_repo_script)
