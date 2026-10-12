# rpi5-ros2-os

A custom Linux OS for the **Raspberry Pi 5**, built with **Yocto (scarthgap 5.0 LTS)**, with SSH access and **ROS 2 Jazzy**. It ships with an example ROS 2 package: a counter publisher/subscriber that can be started and stopped through a service.

## Images

Prebuilt images are attached to [Releases](https://github.com/AndriyAntonenko/rpi5-ros2-os/releases).

| Image | Contents |
|---|---|
| `rpi5-base-image` | Minimal OS: systemd, OpenSSH, Wi-Fi/Ethernet (DHCP), mDNS (avahi), `sudo` |
| `rpi5-ros-image` | Everything in the base image, plus ROS 2 Jazzy (`ros-core`), the official demo nodes, and `counter_demo` |

Both images boot from a **USB drive**. See [Known limitations](#known-limitations).

## Quick start

### 1. Flash

Write the image to a USB drive with [balenaEtcher](https://etcher.balena.io/), which accepts `.wic.bz2` directly, or with `dd`:

```bash
# macOS example: find the drive with `diskutil list` and double-check the number
diskutil unmountDisk /dev/diskN
bzcat rpi5-ros-image-raspberrypi5.rootfs.wic.bz2 | sudo dd of=/dev/rdiskN bs=4m
```

### 2. Configure

No credentials are baked into the image. Re-plug the drive and copy your own files onto the FAT `boot` partition. Templates are in [`boot-files/`](boot-files):

| File on `boot` | Purpose |
|---|---|
| `authorized_keys` | Your SSH public key(s) for the user `andrii`. **Required:** password login is disabled. |
| `wpa_supplicant.conf` | Wi-Fi network and password. Optional if you use Ethernet. |

On every boot, `boot-config.service` copies these files into place before Wi-Fi and SSH start.

### 3. Boot and connect

Plug the drive into a USB 3.0 (blue) port, power on, and wait about a minute:

```bash
ssh andrii@rpi5-yocto.local   # or use the IP address from your router's client list
```

### 4. Run ROS 2

```bash
. /opt/ros/jazzy/setup.sh                    # or add this line to ~/.profile
ros2 launch counter_demo counter.launch.py   # publisher + subscriber
```

In a second SSH session:

```bash
. /opt/ros/jazzy/setup.sh
ros2 node list                               # /counter_publisher, /counter_subscriber
ros2 topic echo /counter
ros2 run counter_demo counter_control stop   # pause the counter
ros2 run counter_demo counter_control start  # resume it
```

## Repository layout

```
.
├── layers/
│   ├── poky/                 # submodule: Yocto core + bitbake
│   ├── meta-openembedded/    # submodule: extra packages
│   ├── meta-raspberrypi/     # submodule: Raspberry Pi BSP
│   ├── meta-ros/             # submodule: ROS 2 recipes
│   └── meta-rpi5-custom/     # this project's layer
├── ros2_ws/                  # ROS 2 workspace: counter_demo + Docker dev environment
└── boot-files/               # templates for the boot partition
```

### `meta-rpi5-custom`

| Path | Purpose |
|---|---|
| `conf/templates/default/` | `bblayers.conf` / `local.conf` templates (machine, systemd, ROS distro, USB boot) |
| `recipes-core/images/rpi5-base-image.bb` | Base image: SSH, networking, user |
| `recipes-core/images/rpi5-ros-image.bb` | Base image plus ROS 2 and `counter_demo` |
| `recipes-core/andrii-user/` | User `andrii`: key-only SSH, passwordless `sudo` |
| `recipes-core/boot-config/` | Service that applies `authorized_keys` and `wpa_supplicant.conf` from `/boot` |
| `recipes-connectivity/wifi-config/` | systemd-networkd DHCP for Ethernet and Wi-Fi; `wpa_supplicant@wlan0` |
| `recipes-ros/counter-demo/` | Builds `ros2_ws/src/counter_demo` (`ament_python`) |
| `wic/rpi5-usb.wks` | Partition layout for booting from `/dev/sda` |

## Building from source

**Host:** Ubuntu 22.04 or 24.04 (x86_64). Plan for 8+ cores, 32 GB RAM and about 250 GB of free disk. The first build takes several hours; rebuilds are incremental.

```bash
sudo apt install -y gawk wget git diffstat unzip texinfo gcc build-essential chrpath \
  socat cpio python3 python3-pip python3-pexpect xz-utils debianutils iputils-ping \
  python3-git python3-jinja2 python3-subunit zstd lz4 file locales libacl1
sudo locale-gen en_US.UTF-8
```

On Ubuntu 24.04 only, allow BitBake to use user namespaces:

```bash
echo "kernel.apparmor_restrict_unprivileged_userns = 0" | sudo tee /etc/sysctl.d/60-bitbake-userns.conf
sudo sysctl --system
```

Build as a non-root user:

```bash
git clone --recurse-submodules https://github.com/AndriyAntonenko/rpi5-ros2-os.git
cd rpi5-ros2-os
TEMPLATECONF=$PWD/layers/meta-rpi5-custom/conf/templates/default \
  source layers/poky/oe-init-build-env build
bitbake rpi5-base-image rpi5-ros-image
```

The images are written to `build/tmp/deploy/images/raspberrypi5/*.rootfs.wic.bz2`.

## ROS 2 package: `counter_demo`

| Executable | Role |
|---|---|
| `counter_publisher` | Publishes `std_msgs/Int64` on `/counter`. Serves `std_srvs/SetBool` on `/counter/set_running`. |
| `counter_subscriber` | Subscribes to `/counter` and logs the values |
| `counter_control start\|stop` | Service client that starts or stops the counter |

`counter_publisher` has these parameters:

| Parameter | Default | Notes |
|---|---|---|
| `period` | `1.0` | Publish period in seconds; can be changed at runtime |
| `start_value` | `0` | Starting value; read-only |
| `start_running` | `true` | Whether to start counting immediately |

`launch/counter.launch.py` starts the publisher and subscriber. It loads `config/params.yaml` and accepts the `period`, `namespace` and `params_file` arguments.

### Development with Docker

```bash
cd ros2_ws
docker build -t counter-demo .
docker run -it --rm --name ros2 counter-demo ros2 launch counter_demo counter.launch.py
```

## Known limitations

- **USB boot only.** The kernel command line uses `root=/dev/sda2`, so the images don't boot from an SD card.
- **Wi-Fi power save is enabled** (`brcmfmac`). The Pi can be slow to answer incoming connections, especially right after boot. Workaround: wait a minute, or run `sudo /usr/sbin/iw dev wlan0 set power_save off` after logging in.
- **mDNS (`rpi5-yocto.local`) may not resolve** on some networks. If it doesn't, use the IP address from your router.
- The Wi-Fi firmware rejects the regulatory country setting and falls back to world-safe defaults, so some 5 GHz channels may be unavailable.
- The user name is fixed to `andrii`.
