import datetime
import sqlite3
import os
from os.path import expanduser

# Click: API Documentation
import click

# GLOBAL VARIABLES
DBPATH = os.path.join(expanduser('~'), 'pcal.db')  # StackAbuse: Python SQLite3 Tutorial


def makedb():
  # Python Docs: SQLite3
  conn = sqlite3.connect(DBPATH)
  c = conn.cursor()

  c.execute('''CREATE TABLE IF NOT EXISTS projects (
      class varchar(255),
      projectname varchar(255),
      file varchar(255),
      duedate date,
      submissions int,
      initpath varchar(255)
    )''')

  conn.commit()
  conn.close()


makedb()


@click.group()
@click.version_option()
def cli():
  """Program Calendar for Autograder"""


@cli.command()
def init():
  """Initializes a pcal directory"""
  conn = sqlite3.connect(DBPATH)
  c = conn.cursor()

  # refactor length search
  c.execute('SELECT COUNT (initpath) FROM projects WHERE initpath=(?);', (os.getcwd(),))
  length = c.fetchone()[0]

  if length > 0:
    click.echo('path already initialized')

  else:
    class_name = input('class: ')
    project_name = input("project name: ")
    project_file = input("project file: ")
    # Python Docs: SQLite3

    # Python Docs: datetime/string formatting
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # replace with dates from Autograder

    project_info = (class_name, project_name, project_file, date, 9999999, str(os.getcwd()))
    c.execute(f'''INSERT INTO projects VALUES (?,?,?,?,?,?)''', project_info)

  conn.commit()
  conn.close()


@cli.command()
def setup():
  """Completes Autograder setup"""
  click.echo('Connecting to autograder...')


@cli.command()
@click.argument('pnames', nargs=-1)
@click.option('-f', '--force', is_flag=True, help='Overrides safety checks before submission')
def submit(pnames, force):

  conn = sqlite3.connect(DBPATH)
  c = conn.cursor()

  """Performs error checking & submits project file to Autograder"""
  if not force:
    # check validity of file submission
    click.echo('error checking...')
    pass

  for project in pnames:
    metadata = c.execute('''SELECT (initpath, file) FROM projects WHERE projectname=(?)''', (project,)).fetchone()

    path = metadata[0]
    file = metadata[1]

    os.chdir(path)
    # submit <file>
    click.echo(f'{project} submitted')

  conn.commit()
  conn.close()


@cli.command()
@click.option('-p', '--path', is_flag=True, help='Adds path to status table')
def status(path):
  """Lists all projects by due date"""
  conn = sqlite3.connect(DBPATH)
  c = conn.cursor()

  projects = list(c.execute('''SELECT * FROM projects ORDER BY duedate'''))

  if len(projects) == 0:
    click.echo('No projects due for now!')

  elif path:
    # Python Docs: String Formatting
    title = ('class', 'project', 'filename', 'date', 'time', 'submissions', 'path')
    click.echo('{0:<7}| {1:<8}| {2:<9}| {3:<11}| {4:<9}| {5:<12}| {6:<10}'.format(*title))

    for row in projects:
      time = row[3].split(' ')
      temp_row = (row[0], row[1], row[2], time[0], time[1], row[4], row[5])

      click.echo('{0:<7}| {1:<8}| {2:<9}| {3:<11}| {4:<9}| {5:<12}| {6:<10}'.format(*temp_row))

  else:
    # Python Docs: String Formatting
    title = ('class', 'project', 'filename', 'date', 'time', 'submissions')
    click.echo('{0:<7}| {1:<8}| {2:<9}| {3:<11}| {4:<9}| {5:<10}'.format(*title))

    for row in projects:
      time = row[3].split(' ')
      temp_row = (row[0], row[1], row[2], time[0], time[1], row[4])

      click.echo('{0:<7}| {1:<8}| {2:<9}| {3:<11}| {4:<9}| {5:<10}'.format(*temp_row))

  conn.commit()
  conn.close()


@cli.command()
@click.argument('pname', required=True)
def remove(pname):
  """Removes a project"""
  conn = sqlite3.connect(DBPATH)
  c = conn.cursor()

  # refactor length search
  c.execute('SELECT COUNT (projectname) FROM projects WHERE projectname=(?);', (pname,))
  length = c.fetchone()[0]

  path = str(c.execute('SELECT (initpath) FROM projects WHERE projectname=(?);', (pname,)).fetchone())

  if length == 0:
    click.echo('project does not exist')
    return ""

  else:
    c.execute('DELETE FROM projects WHERE projectname=(?);', (pname,))

  conn.commit()
  conn.close()

  return path


@cli.command()
def clear():
  """Used for testing purposes"""
  conn = sqlite3.connect(DBPATH)
  c = conn.cursor()

  c.execute('DELETE FROM projects;')

  conn.commit()
  conn.close()


if __name__ == '__main__':
  cli(prog_name='pcal')
