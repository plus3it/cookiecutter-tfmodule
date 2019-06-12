import subprocess

if __name__ == "__main__":
{% if cookiecutter.create_repo == "yes" %}
    subprocess.check_call(['git', 'init'])
    subprocess.check_call(['hub', 'create'])
{%- else %}
    pass
{% endif %}
