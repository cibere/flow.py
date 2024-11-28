import os

import click, json, uuid


@click.group
def cli(): ...

@cli.group(name="create", help="Create specific files")
def create_group(): ...

@create_group.command(name="plugin.json", help="Creates a new plugin.json file")
def create_file() -> None:
    name = input("Plugin Name\n> ")
    desc = input("Plugin Description\n> ")
    author = input("Author Name\n> ")
    plugin_website = input("Plugin Website\n> ")
    icon_path = input("Icon Path (leave blank for `Images/app.png`)\n> ")
    main_file = input("What file should flow execute to start the plugin? Leave blank for `main.py`\n> ")
    data = {
        "ID": uuid.uuid4(),
        "ActionKeyword": "test",
        "Name": name,
        "Description": desc,
        "Author": author,
        "Version": "0.0.1",
        "Language": "python_v2",
        "Website": plugin_website,
        "IcoPath": icon_path,
        "ExecuteFileName": main_file
    }
    with open("plugin.json", "w") as f:
        json.dump(data, f)

@create_group.group("gh", help="Create files in the .github directory")
def create_gh_file_group(): ...

@create_gh_file_group.group("issue_template", help="Github issue templates")
def create_issue_template_group(): ...

@create_issue_template_group.command(name="bug_report", help="Create a detailed bug report template for github issues")
def create_bug_report_issue_template():
    content = f"""
name: Bug Report
description: Report broken or incorrect behaviour
labels: unconfirmed bug
body:
    - type: markdown
        attributes:
        value: >
            Thanks for taking the time to fill out a bug.

            Please note that this form is for bugs only!
    - type: input
        attributes:
            label: Summary
            description: A simple summary of your bug report
        validations:
            required: true
    - type: textarea
        attributes:
            label: Reproduction Steps
            description: >
                What you did to make it happen.
        validations:
            required: true
    - type: textarea
        attributes:
            label: Minimal Reproducible Code
            description: >
                A short snippet of code that showcases the bug.
        render: python
    - type: textarea
        attributes:
            label: Expected Results
            description: >
                What did you expect to happen?
        validations:
            required: true
    - type: textarea
        attributes:
            label: Actual Results
            description: >
                What actually happened?
        validations:
            required: true
    - type: textarea
        attributes:
            label: Flow Launcher Version
            description: Go into your flow launcher settings, go into the about section, and the version should be at the top.
        validations:
            required: true
    - type: textarea
        attributes:
            label: Python Version/Path
            description: Go into your flow launcher settings, go to the general section, and scroll down until you find the `Python Path` field. Copy and paste the value here.
        validations:
            required: true
    - type: textarea
        attributes:
            label: If applicable, Flow Launcher Log File
            description: Use the `Open Log Location` command with the `System Commands` plugin to open the log file folder, and upload the newest file here.
    - type: textarea
        attributes:
            label: Flogin Log File
            description: Use the `Flow Launcher UserData Folder` command with the `System Commands` plugin to open your userdata folder, go into the `Plugins` folder, then find the plugin and go into it. If the `flogin.log` file exists, upload it here. Otherwise please state that it was not there.
    - type: checkboxes
        attributes:
            label: Checklist
            description: >
                Let's make sure you've properly done due diligence when reporting this issue!
            options:
                - label: I have searched the open issues for duplicates.
                required: true
                - label: I have shown the entire traceback, if possible.
                required: true
                - label: I have removed my token from display, if visible.
                required: true
    - type: textarea
        attributes:
            label: Additional Context
            description: If there is anything else to say, please do so here.
    """.strip()
    if not os.path.isdir(".github"):
        os.mkdir(".github")
    if not os.path.isdir(".github/ISSUE_TEMPLATE"):
        os.mkdir(".github/ISSUE_TEMPLATE")
    
    with open(".github/ISSUE_TEMPLATE/bug_report.yml", "w") as f:
        f.write(content)

@create_gh_file_group.command(name="pr_template", help="Create a basic PR template")
def pr_template():
    content = """
## Summary

<!-- What is this pull request for? Does it fix any issues? -->

## Checklist

<!-- Put an x inside [ ] to check it, like so: [x] -->

- [ ] If code changes were made then they have been tested.
    - [ ] I have updated the documentation to reflect the changes.
- [ ] This PR fixes an issue.
- [ ] This PR adds something new (e.g. new method or parameters).
- [ ] This PR is a breaking change (e.g. methods or parameters removed/renamed)
- [ ] This PR is **not** a code change (e.g. documentation, README, ...)
    """.strip()
    if not os.path.isdir(".github"):
        os.mkdir(".github")
    
    with open(".github/PULL_REQUEST_TEMPLATE.md", "w") as f:
        f.write(content)

@create_gh_file_group.group("workflows", help="Create github workflows")
def create_gh_workflows_group(): ...

@create_gh_workflows_group.command(name="publish_release", help="A standard workflow to publish and release a new version of your plugin")
@click.option(
    "--changelog",
    is_flag=True,
    help="If passed, a `CHANGLOG.txt` file will be created in the root directory. When the workflow gets run, the contents of that file will be used as the release's changelog/description."
)
def create_publish_and_release_workflow(changelog: bool = False):
    content = """
name: Publish and Release

on:
  workflow_dispatch:

jobs:
  publish:
    runs-on: ubuntu-latest
    env:
      python_ver: 3.11
    permissions:
      contents: write

    steps:
      - uses: actions/checkout@v2

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v2
        with:
          python-version: ${{ matrix.python-version }}

      - name: get version
        id: version
        uses: notiz-dev/github-action-json-property@release
        with: 
          path: 'plugin.json'
          prop_path: 'Version'

      - run: echo ${{steps.version.outputs.prop}} 

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r ./requirements.txt -t ./lib
          zip -r ${{ github.event.repository.name }} . -x '*.git*'

      - name: Publish
        if: success()
        uses: softprops/action-gh-release@v2
        with:
          files: '${{ github.event.repository.name }}.zip'
          tag_name: "v${{steps.version.outputs.prop}}"
    """.strip()
    if changelog:
        content += "\n          body_path: 'CHANGELOG.txt'"
        with open("CHANGELOG.txt", "w") as f:
            f.write(f"# v0.0.1")

    if not os.path.isdir(".github"):
        os.mkdir(".github")
    if not os.path.isdir(".github/workflows"):
        os.mkdir(".github/workflows")
    
    with open(".github/workflows/publish_release.yml", "w") as f:
        f.write(content)

if __name__ == "__main__":
    cli()
