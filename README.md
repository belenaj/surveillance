# surveillance
This is a Surveillance Project for Raspberry Pi.

Part of this source code is taken from:

http://www.pyimagesearch.com/2015/06/01/home-surveillance-and-motion-detection-with-the-raspberry-pi-python-and-opencv

The structure of the project is as follows:

* pi_surveillance.py
* testing_video.py
* conf.json
* pyimagesearch
  * \_\_init\_\_.py
  * tempimage.py
* video
  * README.txt
  * helicopter.avi

To launch the programs use:

`python pi_surveillance.py --conf conf.json`
`python testing_video.py --conf conf.json`

### Features
* When it detects motion, it sends a notification/email
* When motion is detected, the program starts storing/streaming video
* Camera hardware is not needed to test the software

### TO DO's

- [x] Creating project structure
- [x] Adding files
- [ ] Including changes
- [ ] Testing

###### Notes
The previous dropbox connection is removed.



###### JSON Structure

- This JSON configuration file stores a bunch of important variables. Let’s look at each of them:
- show_video : A boolean indicating whether or not the video stream from the Raspberry Pi should be displayed to our screen.
- min_upload_seconds : The number of seconds to wait in between uploads. For example, if an image was uploaded to Dropbox 5m 33s after starting our script, a second image would not be uploaded until 5m 36s. This parameter simply #controls the frequency of image uploads.
- min_motion_frames : The minimum number of consecutive frames containing motion before an image can be uploaded to Dropbox.
- camera_warmup_time : The number of seconds to allow the Raspberry Pi camera module to “warmup” and calibrate.
- delta_thresh : The minimum absolute value difference between our current frame and averaged frame for a given pixel to be “triggered” as motion. Smaller values will lead to more motion being detected, larger values to less #motion detected.
- resolution : The width and height of the video frame from our Raspberry Pi camera.
- fps : The desired Frames Per Second from our Raspberry Pi camera.
- min_area : The minimum area size of an image (in pixels) for a region to be considered motion or not. Smaller values will lead to more areas marked as motion, whereas higher values of min_area  will only mark larger regions as #motion.

