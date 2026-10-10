## Running Test Cases

To run the test cases for this project, follow the steps below:

### Prerequisites
1. Ensure you have Python 3.10 or higher installed.
2. Install the SDK with its framework and test dependencies (or run `make setup`, which does the same in a virtual environment):
   ```sh
   python3 -m pip install -e ".[flask,fastapi,django,dev]"
   ```

### Setting Up Environment Variables
1. Set the following environment variables in .env file:
   - `DEV_SCALEKIT_ENV_URL`: Your Scalekit environment URL.
   - `DEV_SCALEKIT_CLIENT_ID`: Your Scalekit client ID.
   - `DEV_SCALEKIT_CLIENT_SECRET`: Your Scalekit client secret.


### Running Tests
Use the unittest module to discover and run all test cases:  
```py
python3 -m unittest discover -s tests
```
To run a specific test file, use:  
```py
python3 -m unittest discover -s tests -p "test_file_name.py"
```
