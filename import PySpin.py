import pyspin
import numpy as np
import cv2

# Initialize Spinnaker SDK
system = pyspin.System.GetInstance()
cam_list = system.GetCameras()

# Connect to FLIR camera
cam = cam_list.GetByIndex(0)
cam.Init()

# Configure camera parameters
cam.AcquisitionMode.SetValue(pyspin.AcquisitionMode_Continuous)
cam.PixelFormat.SetValue(pyspin.PixelFormat_Mono16)
cam.TLStream.StreamBufferHandlingMode.SetValue(pyspin.StreamBufferHandlingMode_NewestOnly)

# Start image acquisition
cam.BeginAcquisition()

# Retrieve thermal image from FLIR camera
image = cam.GetNextImage()

# Convert raw thermal image data to numpy array
width = image.GetWidth()
height = image.GetHeight()
img_data = image.GetData()
img = np.ndarray(buffer=img_data,
                 dtype=np.uint16,
                 shape=(height, width))

# Convert numpy array to OpenCV image
cv_img = cv2.applyColorMap(np.uint8(img / 256), cv2.COLORMAP_JET)

# Display OpenCV image in a window
cv2.imshow('FLIR Thermal Image', cv_img)
cv2.waitKey(0)

# Clean up Spinnaker SDK
image.Release()
cam.EndAcquisition()
cam.DeInit()
del cam
cam_list.Clear()
system.ReleaseInstance()
