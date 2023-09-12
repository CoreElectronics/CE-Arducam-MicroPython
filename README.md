This is the Repo for the Core Electronics port of the Arducam Mega 5MP Camera for the Raspberry Pi Pico (Micropython)

Status: **Experimental**
This driver is very much experimental at the moment. Expect frequent, breaking updates.
This project is featured in the 27-July-2023 episode of [The Factory](https://youtu.be/M_b3kmnjF9Y) - Core Electronics' Engineering and Product Development vlog.

<a href="http://www.youtube.com/watch?feature=player_embedded&v=M_b3kmnjF9Y" target="_blank">
 <img src="http://img.youtube.com/vi/M_b3kmnjF9Y/mqdefault.jpg" alt="Watch the video" width="240" height="180" border="10" />
</a>

Project Status:
- [ ] Confirmed working on 3MP Camera (ISSUE: Photos have a green hue, camera_idx identifies the two versions)
- [x] Can set resolution
- [ ] Can set remaining filters and modes
- [ ] Class moved to separate file
- [ ] Burst read
- [ ] Confirm a micro SD card can use the same SPI bus (Micropython compatibility)
- [ ] Confirm working with latest Micropython version)
- [ ] Filemanager also handles subfolders for images
- [ ] Confirm that different file formats output correctly (RGB=BMP, YGV?)
- [ ] Confirm that pixel RGB values can be extrapolated from BMP format for machine learning applications

# License
This project is open source - please review the LICENSE.md file for further licensing information.

If you have any technical questions, or concerns about licensing, please contact technical support on the [Core Electronics forums](https://forum.core-electronics.com.au/).
