This is the Repo for the Core Electronics port of the Arducam Mega Cameras for the Raspberry Pi Pico (Micropython)
* [ArduCam Mega 5MP Camera](https://core-electronics.com.au/arducam-mega-5mp-camera.html)
* [ArduCam Mega 3MP Camera](https://core-electronics.com.au/arducam-mega-3mp-camera.html)

Status: **Experimental**
This driver is very much experimental at the moment. Expect frequent, breaking updates.
This project is featured in the 27-July-2023 episode of [The Factory](https://youtu.be/M_b3kmnjF9Y) - Core Electronics' Engineering and Product Development vlog.

<a href="http://www.youtube.com/watch?feature=player_embedded&v=M_b3kmnjF9Y" target="_blank">
 <img src="http://img.youtube.com/vi/M_b3kmnjF9Y/mqdefault.jpg" alt="Watch the video" width="240" height="180" border="10" />
</a>

## Contributions:

Thank you to @[chrisrothwell1](https://github.com/chrisrothwell1) for getting burst reads working - significantly removing the same time for each image (https://github.com/CoreElectronics/CE-Arducam-MicroPython/issues/9)

Thank you to @[wil-liammacleod](https://github.com/wil-liammacleod) for adding debug mode, a pin reference for the ESP32-S3 and testing on MicroPython 1.24 (https://github.com/CoreElectronics/CE-Arducam-MicroPython/pull/11)

Thank you to @[koyuul](https://github.com/koyuul) for fixing up some errors, allowing `main.py` to be run out of the box, and adding an example for using many Cameras on the same SPI interface.



Project Status:
- [ ] Can set remaining filters and modes - with setters and getters
- [x] Able to set multiple adjustments at the same time ([Ought to be addressed](https://github.com/CoreElectronics/CE-Arducam-MicroPython/issues/3))
- [x] SOLVED: Burst read - decrease time to save photo - Thank you @[chrisrothwell1](https://github.com/chrisrothwell1)
- [ ] Confirm a micro SD card can use the same SPI bus (Micropython compatibility) - requires camera to release SPI bus, bulk reading/writing into bytearray would speed this up
- [ ] Filemanager also handles subfolders for images - Requires examples
- [ ] Confirm that different file formats output correctly (RGB=BMP, YGV?)
- [ ] Confirm that pixel RGB values can be extrapolated from BMP format for machine learning applications


## Details

`Camera(spi_bus=, cs=, skip_sleep=False, debug_text_enabled=False)`
The Cameras initialisation method.

Parameter | Type | Range            | Default                               | Description
--------- | ---- | ---------------- | ------------------------------------- | --------------------------------------------------
spi_bus   | SPI  | Device dependent | N/A                                   | The SPI Bus the camera is connected to.
cs        | Pin  | Device dependent | N/A                                   | The Pin the CS wire is connected to.
skip_sleep | Boolean  | True, False  | False                                | Skips the auto-white-balance on the 5MP Mega
debug_text_enabled | Boolean | True, False  | False                         | If enabled, prints the status of the camera

`Camera.capture_jpg()`
Capture a JPG photo with the provided settings.

`Camera.save_JPG(filename, progress_bar=True)`
Requires `Camera.capture_jpg()` to be run first, saves the JPG to the filename provided (it should include the filetype extension `.jpg`.
Note: This function can over-write other photos, we recommend using the filemanager.

Parameter | Type | Range            | Default                               | Description
--------- | ---- | ---------------- | ------------------------------------- | --------------------------------------------------
filename  | str  | N/A              | 'image.jpg'                           | The file path for the image.
progress_bar | Boolean | True, False | True                                 | Prints a progress bar as the image saves.

# License
This project is open source - please review the LICENSE.md file for further licensing information.

If you have any technical questions, or concerns about licensing, please contact technical support on the [Core Electronics forums](https://forum.core-electronics.com.au/).
