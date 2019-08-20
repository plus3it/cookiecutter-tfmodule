# cookiecutter-tf-module

Cookiecutter template to manage consistent creation of Terraform modules.

## To use this template

```bash
$ pip install cookiecutter GitPython hub python-terraform
$ cookiecutter https://github.com/plus3it/cookiecutter-tfmodule.git
```

You will be prompted for basic info (your name, module name, etc.) which will be used in the template.

That's all you need to get started.

## Testing the module

The `tests` folder implements a simple test harness.

In order to use the testing suite you will need to do the following:

0. Write test cases that use the module, placing each test case in its own directory under `tests/`, e.g. `tests/<test_case1>`
1. Install `go`
2. Run `make dep/install` to install dep
3. Run `make terratest/install` to install the prerequisites.
4. Run `make terratest/test` for your suite of tests to run

### Example test case
For the most part, you will create simple terraform code that will just instantiate your module
```terraform
module "example_1" {
  source = "../../"

  variable_1 = "alpha"
  variable_2 = "beta"
}
```

Additional test cases will typically alter the variables passed to the module to address other scenarios
```terraform
module "example_2" {
  source = "../../"

  variable_1 = "alpha"
  variable_2 = "gamma"
}
```

### Test case prerequisites
In certain situations you may need some pre-existing infrastructure to exist in order to fulfill your test case.
In those cases please setup the following for your prerequisite infrastructure to be setup

1. Create a `prereq` directory within your specific test case folder (e.g., <module_name>/tests/<testcase_name>/prereq)
2. Create the requisite terraform code to create the prerequisite infrastructure (e.g., <module_name>/tests/<testcase_name>/prereq/main.tf)
3. Use a `terraform_remote_state` resource in your testcase code to reference materials created within the prerequisite code
  ```terraform
  data "terraform_remote_state" "prereq" {
    backend = "local"
    config = {
      path = "prereq/terraform.tfstate"
    }
  }

  module "example" {
    source = "../../"

    name             = "${data.terraform_remote_state.prereq.random_name}"
  }
  ```

## Inputs

You will be asked for these fields:

| Template Variable  | Default | Description |
| ------------------ | ------- | ----------- |
| ``create_repo`` | ``no`` | Whether or not to automatically create a repo on GitHub. |
| ``create_org_repo`` | ``no`` | Whether or not to automatically create an organizational repo on GitHub. |
| ``github_readonly_token`` | ``null`` | GitHub OATH Token to make informational API calls. |
| ``github_releases_token`` | ``null`` | GitHub OATH Token used to automatically tag repo on a pull request approval. |
| ``github_username`` | ``plus3it`` | Your GitHub Username. |
| ``module_name`` | ``template`` | The name of the terraform module that you are creating. |
| ``short_description`` | ``A Terraform Module`` | Description of the terraform module. |

## Examples

You can find example terraform modules at `https://github.com/search?q=plus3it%2Fterraform-aws-tardigrade`
