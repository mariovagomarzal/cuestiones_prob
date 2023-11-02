from invoke import task


@task
def clean(c):
    c.run("latexmk -C")


@task
def build(c):
    c.run("latexmk main.tex")
