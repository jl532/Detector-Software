'''
Video feed and single shots from Basler camera in openCV
Tested on acA3088
'''

from pypylon import pylon
import cv2

def liveView(gain, exposure, digitalShift, bitDepth):
    '''
    Shows live feed in cv2 window, exits when escape key is pressed
    Parameters: Gain (db), Exposure (ms), Digital Shift (int multiple), bitDepth (string)
    bitDepth options: "Mono8", "Mono12", "Mono12p"
    '''
    
    # Grabs first camera available, intiates
    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
    camera.Open()

    # Sets camera parameters for live viewing
    camera.Gain = gain
    camera.ExposureTime = exposure
    camera.DigitalShift = digitalShift
    camera.PixelFormat = bitDepth

    # Set up impage processing for OpenCV
    converter = pylon.ImageFormatConverter()
    converter.OutputPixelFormat = pylon.PixelType_BGR8packed
    converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

    # Start video feed
    camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

    # Processing loop
    while camera.IsGrabbing():
        # Store image data
        buffer = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
        if buffer.GrabSucceeded():
            # Convert to openCV format
            frame = converter.Convert(buffer)
            frame_arr = frame.GetArray()
            # Open window for feed and present frame
            cv2.namedWindow("Live view (" + camera.GetDeviceInfo().GetModelName() + ")", cv2.WINDOW_NORMAL)
            cv2.imshow("Live view (" + camera.GetDeviceInfo().GetModelName() + ")", frame_arr)
            # Exit if escape key (27) is pressed
            key = cv2.waitKey(1) # Frame from imshow lasts for one ms
            if key == 27: break
        buffer.Release()

    # Close procedure
    camera.StopGrabbing()
    camera.Close()
    cv2.destroyAllWindows()

def singleCapture(gain, exposure, digitalShift, bitDepth):
    '''
    Takes single shot and opens in cv2 window, exits when key is pressed
    Parameters: Gain (db), Exposure (ms), Digital Shift (int multiple), bitDepth (string)
    bitDepth options: "Mono8", "Mono12", "Mono12p"
    '''
    
    # Grabs first camera available, intiates
    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
    camera.Open()

    # Sets camera parameters for live viewing
    camera.Gain = gain
    camera.ExposureTime = exposure
    camera.DigitalShift = digitalShift
    camera.PixelFormat = bitDepth

    # Set up impage processing for OpenCV
    converter = pylon.ImageFormatConverter()
    converter.OutputPixelFormat = pylon.PixelType_BGR8packed
    converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

    buffer = camera.GrabOne(int(camera.ExposureTime.Value))
    if buffer:
        # Convert to openCV format
        frame = converter.Convert(buffer)
        frame_arr = frame.GetArray()
        # Open window for feed and present frame
        cv2.namedWindow("Snapshot (" + camera.GetDeviceInfo().GetModelName() + ")", cv2.WINDOW_NORMAL)
        cv2.imshow("Snapshot (" + camera.GetDeviceInfo().GetModelName() + ")", frame_arr)
        cv2.waitKey(0)
    buffer.Release()

    # Close procedure
    camera.Close()
    cv2.destroyAllWindows()

# - - - - 
singleCapture(12, 1e4, 4, "Mono12p")
liveView(12, 1e4, 4, "Mono12p")

