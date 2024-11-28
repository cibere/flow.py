Command Line Interface
=======================
Flogin provides some CLI commands to easily and quickly make new plugins.

.. function:: flogin create [OPTIONS] COMMAND [ARGS]

    Create specific files

    Options:
        --help
            Show this message and exit.

    Commands:
        `gh <#create-gh>`_
            Create files in the .github directory
        `plugin.json <#create-plugin-json>`_
            Creates a new plugin.json file

create plugin.json
~~~~~~~~~~~~~~~~~~

.. function:: flogin create plugin.json [OPTIONS]

    Creates a new ``plugin.json`` file

    Options:
        --help
            Show this message and exit.

create gh
~~~~~~~~~~

.. function:: flogin create gh [OPTIONS] COMMAND [ARGS]

    Create files in the ``.github`` directory

    Options:
        --help
            Show this message and exit.

    Commands:
        `issue_template <#create-gh-issue-template>`_
            Github issue templates
        `pr_template <#create-gh-pr-template>`_
            Create a basic PR template
        `workflows <#create-gh-workflows>`_
            Create github workflows

create gh issue_template
~~~~~~~~~~~~~~~~~~~~~~~~

.. function:: flogin create gh issue_template [OPTIONS] COMMAND [ARGS]

    Github issue templates

    Options:
        --help
            Show this message and exit.

    Commands:
        `bug_report <#create-gh-issue_template-bug-report>`_
            Create a detailed bug report template for github issues

create gh issue_template bug_report
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. function:: flogin create gh issue_template bug_report [OPTIONS]

    Create a detailed bug report template for github issues

    Options:
        --help
            Show this message and exit.

create gh pr_template
~~~~~~~~~~~~~~~~~~~~~

.. function:: flogin create gh pr_template [OPTIONS]

    Create a basic PR template

    Options:
        --help
            Show this message and exit.

create gh workflows
~~~~~~~~~~~~~~~~~~~

.. function:: flogin create gh workflows [OPTIONS] COMMAND [ARGS]

    Create github workflows

    Options:
        --help
            Show this message and exit.

    Commands:
        `publish_release <#create-gh-workflows-publish-release>`_
            A standard workflow to publish and release a new version of your plugin

create gh workflows publish_release
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. function:: flogin create gh workflows publish_release [OPTIONS]

    A standard workflow to publish and release a new version of your plugin

    Options:
        --changelog
            If passed, a ``CHANGLOG.txt`` file will be created in the root directory. When the workflow gets run, the contents of that file will be used as the release's changelog/description.
        --help
            Show this message and exit.
