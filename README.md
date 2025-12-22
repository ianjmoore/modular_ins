# Modular INS
ROS 2 interface example for an externally aided tactical grade INS with Dual-Antenna GNSS receiver and RTK corrections via a one-shot launch file.
<br/>

## Bill of Materials

### Hardware

#### INS:
- MicroStrain [CV7-INS](https://www.hbkworld.com/en/products/transducers/inertial-sensors/navigation/3dm-cv7-ins)
- [Black c-series dev board](https://www.hbkworld.com/en/products/transducers/inertial-sensors/accessories/p-6212-3009) 

#### GNSS:
- Septentrio Mosaic GNSS Receiver - either: 
    - [Mosaic Go heading eval kit](https://www.septentrio.com/en/products/gnss-receivers/gnss-receiver-modules/mosaic-h-evaluation-kit) (Mosaic H receiver)
    - [Mosaic Go X5 eval kit](https://www.septentrio.com/en/products/gnss-receivers/gnss-receiver-modules/mosaic-go-evaluation-kit) (Mosaic X5 receiver)
- SMA - SMA GNSS connector cable
- 2x L1/L2 or Full Band GNSS Antennas
- [SensorCloudRTK](https://rtkapp.sensorcloud.com/) API

#### Compute:
- Linux machine running Ubuntu 22.04 or later

### Software:
- [microstrain_inertial](https://github.com/LORD-MicroStrain/microstrain_inertial/tree/ros2) 
- [septentrio_gnss_driver](https://github.com/septentrio-gnss/septentrio_gnss_driver) 
- [ntrip_client](https://github.com/LORD-MicroStrain/ntrip_client/tree/ros2)

## Install Instructions

### Building from Source
1. Install ROS2 and create a workspace: [Configuring Your ROS2 Environment](https://docs.ros.org/en/foxy/Tutorials/Configuring-ROS2-Environment.html)
1. Clone the repository into your workspace:
```bash
git clone https://github.com/ianjmoore/modular_ins.git ~/your_workspace/src/modular_ins
```
3. Install rosdeps for this package: `rosdep install --from-paths ~/your_workspace/src -i -r -y`
1. Build your workspace:
```bash
cd ~/your_workspace
colcon build
source ~/your_workspace/install/setup.bash
```
>[!TIP]
>The source command will need to be run in each terminal prior to launching a ROS node.


## Run Instructions

#### Launch files
Two launch files are provided for recommended use for specific applications: 

1. **Dual Antenna Heading** (GPS compass) with Mosaic H to CV7-INS
    1. Recommended for hovering UAS that require static heading, vehicles with low dynamics, or strong magnetic interference 
        1. Ex: VTOL / Quadcopter UAS, Differential drive wheeled vehicles, QUGV, USV, low jamming & spoofing environments
```bash
ros2 launch modular_ins mosaic_h_cv7_ins_ext_heading.py
```

2. **Full Band GNSS** with Mosaic X5 + CV7-INS **Magnetometer Heading**
    1. Recommended for highest interference / GNSS contested environments (jamming, spoofing), fixed-wing UAS that do not hover, Ackerman steering geometry vehicles, low magnetic interference 
        1. Ex: Fixed-wing UAS, vehicle in known GNSS contested environment, high-multipath lawn mower, few moving ferro-magnetic moving parts near INS
        <br/>
        NOTE: Dual Antenna Heading not supported on Mosaic X5
```bash
ros2 launch modular_ins mosaic_x5_cv7_ins_mag_heading.py
```


## Docker Development

### VSCode

The easiest way to develop in docker while still using an IDE is to use VSCode. Follow the steps below to develop on this repo in a docker container.

1. Install the following dependencies:
    1. [VSCode](https://code.visualstudio.com/)
    1. [Docker](https://docs.docker.com/get-docker/)
1. Open VSCode and install the following [plugins](https://code.visualstudio.com/docs/editor/extension-marketplace):
    1. [VSCode Remote Containers plugin](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
1. Open `/workspace_dir/src/modular_ins/` directory in VSCode
1. A prompt should appear, and click "Reopen in devcontainer"
    1. If not, follow [Docker Troubleshooting](#docker-troubleshooting) below  
1. Once the project is open in the container, it will take some time to automatically install the rosdeps inside the container
1. Build your workspace: 
```bash
# cd ~/your_workspace #TODO: Check if recommended
colcon build
source install/setup.bash
```
>[!TIP]
>The source command will need to be run in each terminal prior to launching a ROS node.
7. Proceed to [Run Instructions](#run-instructions)

#### Docker Troubleshooting 
1. Click the blue `><` icon in the bottom left corner of the window
    1. Choose `Reopen In Container`
1. If that does not work or if VS Code keeps prompting you to open a devcontainer:
1. Close VSCode
1. In terminal, navigate to `/your_workspace_dir/src/modular_ins/`
1. Run `code .`
1. [If prompted] select `modular_ins/.devcontainer/devcontainer.json` as container settings file
1. You should be prompted to "Reopen in devcontainer"
1. If still having troubles, open a ticket on the [MicroStrain Support Portal](https://sensor.support.microstrain.com/servicedesk/customer/portals) or write to [MicroStrainSupport@HBKWorld.com](mailto:MicroStrainSupport@HBKWorld.com)
