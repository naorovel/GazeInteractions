# Docker Setup for Tobii Eye Tracker 5 with ROS Noetic
Provides an environment that contains required dependencies for the Tobii Eye Tracker 5 as well as ROS

## Requirements
You'll need to obtain the following:
1. Tobii Pro SDK C (needs to be in ./tobii/prosdk)
2. Tobii Stream Engine Library (needs to be in ./tobii/streamengine)
3. [multiarch-support_2.27-3ubuntu1.4_amd64.deb](https://launchpad.net/ubuntu/bionic/amd64/multiarch-support/2.27-3ubuntu1.4), libuv0.10_0.10.22-2_amd64.deb, tobii_engine_linux-0.1.6.193_rc-Linux.deb, tobiiusbservice_l64U14_2.1.5-28fd4a.deb, and tobii_config_0.1.6.111_amd64.deb (needs to be in ./tobii/deps)
4. config.db file from a configured eye tracker (in ./tobii/config.db) - provided

The first can be obtained from tobii at https://connect.tobii.com/s/sdk-c-linux-form 

The repo here https://github.com/Eitol/tobii_eye_tracker_linux_installer/tree/master has most of the other dependencies. Libuv0.10 can also be found [here](https://launchpad.net/ubuntu/trusty/i386/libuv0.10/0.10.22-2) with a slightly different version, but likely will work if you update the dockerfile to look for the updated file name.

A `config.db` file can be obtained from the tobii_config tool also found in the above link, and is found in `/usr/share/tobii_engine/db/config.db`
once calibration is complete. You can also configure in the container; see the "Configuration" section

## Usage
First, ensure that the above requirements are placed in the appropriate folders. Then:

`docker compose up --build`

`docker exec -it tobii-ros bash`

Or, in vscode, use the dev containers extension, and select "rebuild and reopen in container". 

**NOTE**: If you are using vscode you should be able to un-comment out the last two lines of the dockerfile that add the eye tracker service start script to bashrc, but this seems to break things if you are using `docker exec`

## Configuration
Configuring the eye tracker will generate a `config.db` file in `/usr/share/tobii_engine/db/config.db`.

A config file should already be included, and is placed in `./tobii`. However, it likely is not optimal for your setup, so you may want to generate a new one.

To configure the eye tracker, open the container, run `./start_et.sh`, and then `/opt/tobii_config/tobii_config` in a terminal to open a config tool. Once configured, this will save the updated file at `/usr/share/tobii_engine/db/config.db`. You can then copy this to `./tobii` to have it be used in future builds.

You likely will need to run `xhost +` in a local terminal before running the eye tracker for this to work.

## Test Scripts:
Located in the `testscripts` directory

First, run `./start_et.sh`. 

Tobii Python Bindings Test: `python3.10 test.py` 

Stream Engine Test: `gcc main.cpp -o main -pthread /usr/lib/tobii/libtobii_stream_engine.so` if not compiled, then `./main`

## Resources
https://tobiitech.github.io/stream-engine-docs/ tobii stream engine library documentation

https://github.com/Eitol/tobii_eye_tracker_linux_installer/tree/master tobii install for 4C (also works for 5 for our case) on linux; contains packages

https://github.com/betaboon/python-tobii-stream-engine for tobii stream engine python bindings installation instructions

https://github.com/letoram/arcan-docker/tree/master as a reference for an existing tobii docker file

https://developer.tobiipro.com/c/c-getting-started.html tobii pro sdk C installation guide
