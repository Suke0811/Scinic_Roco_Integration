#!/bin/bash

# Find Webots in WEBOTS_HOME directory if given; otherwise try likely locations
if [ -n "${WEBOTS_HOME}" ]; then
	if [ ! -x $WEBOTS_HOME/webots ]; then
		echo "could not find Webots executable in WEBOTS_HOME"
		exit 1
	fi
	webots_home=$WEBOTS_HOME
elif [ -x "/Applications/Webots.app/webots" ]; then
	webots_home="/Applications/Webots.app"
elif [ -x "/usr/local/webots/webots" ]; then
	webots_home="/usr/local/webots"
else
	echo "could not find Webots: set WEBOTS_HOME to folder containing it"
	exit 1
fi

# Install Scenic in a virtual environment (if one doesn't already exist)
cd scenic
poetry install
source $(poetry env list --full-path)/bin/activate

# Install RoCo in the virtualenv
cd ../roco
pip install -e .

# Run the simulations
cd ..
$webots_home/webots --batch --mode=fast --stdout --stderr simulation/worlds/RoCo_Moving.wbt
