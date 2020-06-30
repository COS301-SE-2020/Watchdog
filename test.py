import cv2

def get_video(input_id):
    camera = cv2.VideoCapture(input_id)
    while True:
        okay, frame = camera.read()
        if not okay:
            break

        cv2.imshow('video', frame)
        cv2.waitKey(1)
    pass

if __name__ == '__main__':
    get_video('tcp://127.0.0.1:8080')