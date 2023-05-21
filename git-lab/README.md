## Virtual Environment in Python
Python virtual environment is a folder structure that gives you everything you need to run a lightweight yet isolated Python environment.

### Instructions

Follow the instruction

1. Create directory for each component of your application and change it to current working directory
   ```bash
   mkdir -p hello_demo
   cd hello_demo
   ```

2. Verify current working directory
   ```bash
   pwd
   ```

3. Create virtual env
    ```bash
   python3 -m venv venv_hello
   ```

4. Activate virtual env
    ```bash
   source venv_hello/bin/activate
    ```

5. Install required packages
   ```bash
   pip install python-dotenv
   ```

6. Create and Execute the python script
    ```bash
    python3 main.py
    ```

7. Export your packages using
    ```bash
    pip freeze list > requirements.txt
    ```
   To reinstall the python modules from the requirements.txt
    ```bash
    pip install -r requirements.txt
    ```

8.  Duplicate the env file with the name `example.env`
    ```bash
    cp .env example.env
    ```
9.  Strip off the values for the example.env file
    ```bash
    cat example.env
    # Output
    DATABASE_URL=
    DATABASE_USER=
    DATABASE_PASSWORD=
    ```

10. Add the following file names in `.gitignore` file
    ```bash
    # append to .gitignore
    venv_hello 
    .env
    ```

11. Review the changes to be committed to github and push them

12. Open a Pull Request (PR) to merge changes to `main`

13. To deactivate the virtual environment
    ```bash
    deactivate
    ```
14. To reinstall the python modules from the requirements.txt
    ```bash
    pip install -r requirements.txt
    ```
