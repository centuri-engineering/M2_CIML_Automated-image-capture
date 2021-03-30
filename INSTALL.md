# Software installation



This project is tested on a RaspberryPi machine with Raspbian. The user should be authorized to run `sudo`

## Dependencies


Run the following in a terminal:

```bash
sudo apt install libatlas-base-dev\
	libsdl2-dev \
	libsdl2-ttf-dev \
	libsdl2-image-dev \
	libsdl2-mixer-dev 
```


## Download the source of the project, either through git:

```bash
git clone https://github.com/centuri-engineering/M2_CIML_Automated-image-capture.git
```

Or the archive:

```bash
wget https://github.com/centuri-engineering/M2_CIML_Automated-image-capture/archive/refs/heads/main.zip
unzip M2_CIML_Automated-image-capture-main.zip
```

Then go to the RaspberryPi directory and install the project dependencies

```bash
cd RaspberryPi
python3 -m pip install -U -r requirements.txt
```

Make sure the user (if it is not the default `pi`) user belongs to the groups `dialout sudo video input gpio`:
```bash
groups
user_name dialout sudo video input gpio
```


