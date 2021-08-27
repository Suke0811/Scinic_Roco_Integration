# roco\_scenic\_integration
roco scenic integration and debugging 

## Usage

The `run.sh` script installs RoCo and Scenic as needed (creating a new virtual
environment if an appropriate one does not already exist) and runs the pipeline,
placing the results in the `results` directory. The script attempts to find
Webots in its default locations on Linux and macOS; otherwise you must provide
the Webots root directory in the environment variable `WEBOTS_HOME`.
