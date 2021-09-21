from picamera import PiCamera

class Camera:
    def __init__(self):
        camera = PiCamera()
        camera.resolution = (960, 750)
        camera.start_preview()
        a = input()
        camera.capture('1.png')
        camera.stop_preview()

    
