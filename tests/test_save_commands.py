import pytest
import os, sys
import mock
import builtins

workspace_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.abspath(workspace_path))
path = os.path.dirname(__file__)

from save_commands import save_commands


def alter_database_path(db_number):
    save_commands.database_name = '.testing_{}.db'.format(db_number)
    save_commands.database_path = os.path.join(os.getenv("HOME"), save_commands.database_name)


def remove_database(db_number):
    db = '.testing_{}.db'.format(db_number)
    path = os.path.join(os.getenv("HOME"), db)
    if os.path.exists(path):
        os.remove(path)


def test_verify_arguments_sucess():    
    args = ['./cmd.py', 'add', 'cmd1', 'ls', 'list']
    assert type(save_commands.verify_arguments(args)) == dict
    

def test_verify_arguments_error():
    assert type(save_commands.verify_arguments(['./cmd.py', 'add', 'cmd1', 'ls'])) == type(None)
    assert type(save_commands.verify_arguments(['./cmd.py'])) == type(None)
    assert type(save_commands.verify_arguments(['./cmd.py', 'remove'])) == type(None)
    assert type(save_commands.verify_arguments(['./cmd.py', 'help'])) == type(None)


def test_verify_get_connection():
    remove_database(1)
    alter_database_path(1)
    db = os.path.join(os.getenv("HOME"), save_commands.database_name)
    if os.path.exists(db):
        os.remove(db)
    save_commands.get_connection()
    remove_database(1)


def test_action_add():
    remove_database(2)
    alter_database_path(2)
    args = ['./cmd.py', 'add', 'cmd_test', 'ls', 'test command']
    a = save_commands.verify_arguments(args)
    assert save_commands.action_add(a) == True
    remove_database(2)


def test_action_add_exists():
    remove_database(3)
    alter_database_path(3)
    save_commands.database_name = '.testing_db'
    args = ['./cmd.py', 'add', 'cmd_test', 'ls', 'test command']
    a = save_commands.verify_arguments(args)
    save_commands.action_add(a)
    args = ['./cmd.py', 'add', 'cmd_test', 'ls', 'test command']
    a = save_commands.verify_arguments(args)
    assert save_commands.action_add(a) == False
    remove_database(3)


@mock.patch.object(builtins, 'input')
def test_action_remove(mock_input):
    remove_database(4)
    alter_database_path(4)
    args = ['./cmd.py', 'add', 'cmd_test_2', 'ls', 'test command']
    a = save_commands.verify_arguments(args)
    save_commands.action_add(a)
    args = ['./cmd.py', 'remove', 'cmd_test_2']
    mock_input.return_value = 'yes'
    a = save_commands.verify_arguments(args)
    assert save_commands.action_remove(a) == True
    remove_database(4)


def test_action_list():
    remove_database(5)
    alter_database_path(5)
    save_commands.action_list()
    remove_database(5)


def test_action_run():
    remove_database(6)
    alter_database_path(6)
    args = ['./cmd.py', 'add', 'cmd_test_3', 'ls', 'test command']
    a = save_commands.verify_arguments(args)
    save_commands.action_add(a)
    args = ['./cmd.py', 'run', 'cmd_test_3']
    a = save_commands.verify_arguments(args)
    save_commands.action_run(a)
    remove_database(6)


@mock.patch.object(builtins, 'input')
def test_main(mock_input):
    remove_database(7)
    alter_database_path(7)
    args = ['./cmd.py', 'add', 'cmd_test_main', 'ls', 'test command']
    save_commands.main(args)
    args = ['./cmd.py', 'list']
    save_commands.main(args)
    args = ['./cmd.py', 'run', 'cmd_test_main']
    save_commands.main(args)
    args = ['./cmd.py', 'remove', 'cmd_test_main']
    mock_input.return_value = 'yes'
    save_commands.main(args)
    remove_database(7)
