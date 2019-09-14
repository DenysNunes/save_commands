# save_commands

<b>Objective</b>
___
I have all kind of shell commands, over many environments (e.g, ssh in dev for customer 'x' and another for 'y') and did need a repository for save and running this ones easily. 
So, with this tool I can manage and run commands using keys and dont need remember full command.

<b>Requeriments</b>
___

Application was developed using Python 3.7, Fedora 30 and Visual Studio Code.
This tool don't use any external library, only `pytest` was used for testing purpose.

<b>Installation Steps</b>

1. Clone repository:

    ```
    cd ~
    git clone https://github.com/DenysNunes/save_commands.git
    ```

2. Python install:

    ```
    cd ~/save_commands
    sudo python3 setup.py install
    ```
3. Running (like a shell command):
   
   ```
   save-commands help
   ```

<b>Observations:</b>

* The app write all data using Python native sqlite library, a single *.db file is saved in `home` directory.
* All test cases are running over separated and temporary databases.
