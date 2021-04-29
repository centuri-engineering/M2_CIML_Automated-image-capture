import time
from picamerax import PiCamera

from config import Config


def setup_camera(camera=None, **kwargs):
    """Modifies a camera instance or creates one with the settings defined in config"""
    if camera is None:
        camera = PiCamera()
    settings = Config.cam_set.copy()
    settings.update(kwargs)
    for (attr, value) in settings.items():
        setattr(camera, attr, value)

    return camera


def capture(im_path=None, camera=None):
    timestr = time.strftime("%Y%m%d_%H%M%S")
    camera = setup_camera(camera)
    if im_path is None:
        im_path = Config.img_dir / f"cap_{timestr}.jpg"

    with open(im_path, "bw") as fh:
        camera.capture(fh)
    print(f"captured {im_path}")
