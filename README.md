This is the Repo for the Core Electronics port of the Arducam Mega 5MP Camera for the Raspberry Pi Pico (Micropython)

Status: **Experimental**
This driver is very much experimental at the moment. Expect frequent, breaking updates.
This project is featured in the 27-July-2023 episode of [The Factory](https://youtu.be/M_b3kmnjF9Y) - Core Electronics' Engineering and Product Development vlog.

<a href="http://www.youtube.com/watch?feature=player_embedded&v=M_b3kmnjF9Y" target="_blank">
 <img src="http://img.youtube.com/vi/M_b3kmnjF9Y/mqdefault.jpg" alt="Watch the video" width="240" height="180" border="10" />
</a>

Project Status:
- [x] Confirmed working on 3MP Camera
- [x] SOLVED: Photos have a green hue, camera_idx identifies the two versions - https://forum.arducam.com/t/mega-3mp-micropython-driver/5708
- [x] Can set resolution
- [ ] Can set remaining filters and modes
- [ ] Able to set multiple adjustments at the same time ([see issue#3](https://github.com/CoreElectronics/CE-Arducam-MicroPython/issues))
- [ ] Class moved to separate file
- [ ] Burst read - decrease time to save photo
- [ ] Set SPI Speed higher - decrease time to save photo - Recommended speed from ArduCam 800000 baud, need to implement a check on init
- [ ] Confirm a micro SD card can use the same SPI bus (Micropython compatibility) - requires camera to release SPI bus, bulk reading/writing into bytearray would speed this up
- [ ] Confirm working with the latest Micropython version
- [ ] Filemanager also handles subfolders for images - Requires examples
- [ ] Confirm that different file formats output correctly (RGB=BMP, YGV?)
- [ ] Confirm that pixel RGB values can be extrapolated from BMP format for machine learning applications

The Camera library can be created by extracting the 'Camera' class from the [main.py](https://github.com/CoreElectronics/CE-Arducam-MicroPython/blob/main/main.py) file.

# License
This project is open source - please review the LICENSE.md file for further licensing information.

If you have any technical questions, or concerns about licensing, please contact technical support on the [Core Electronics forums](https://forum.core-electronics.com.au/).
