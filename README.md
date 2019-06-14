# cookiecutter-tf-module

Cookiecutter template to manage consistent creation of Terraform modules.

## To use this template

```bash
$ pip install cookiecutter hub
$ cookiecutter https://github.com/plus3it/cookiecutter-tfmodule.git
```

You will be prompted for basic info (your name, module name, etc.) which will be used in the template.

That's all you need to get started.

## Inputs

You will be asked for these fields:

| Template Variable  | Default | Description |
| ------------------ | ------- | ----------- |
| ``create_repo`` | ``yes`` | Whether or not to automatically create a repo on GitHub. |
| ``github_readonly_token`` | ``null`` | GitHub OATH Token to make informational API calls. |
| ``github_releases_token`` | ``null`` | GitHub OATH Token used to automatically tag repo on a pull request approval. |
| ``github_username`` | ``plus3it`` | Your GitHub Username. |
| ``module_name`` | ``template`` | The name of the terraform module that you are creating. |
| ``short_description`` | ``A Terraform Module`` | Description of the terraform module. |

## Examples

You can find example terraform extensive modules at `https://github.com/search?q=plus3it%2Fterraform-aws-tardigrade`
