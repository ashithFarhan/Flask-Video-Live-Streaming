import cv2
import threading 
import time

new_frames = False
next_frame = -1

p=open('placeholder.jpg', 'rb').read()
frames_buffer = [p,p,p]


class Camera(object):
    def __init__(self):
        print('Starting camera')
        self.next = -1

    def get_frame(self):
        global new_frames
        global frames_buffer
        global next_frame
        next_frame = self.next
        self.next = (self.next+1)%3
        new_frames = True
        time.sleep(0.05)
        return frames_buffer[self.next]


def record():
    cap = cv2.VideoCapture(0)
    global new_frames
    global frames_buffer
    global next_frame
    while True:
        if new_frames:
            _, frame = cap.read()
            frame = cv2.flip(frame, 1) # flip horizontally
            _, JPEG = cv2.imencode('.jpeg', frame)
            frames_buffer[next_frame] = JPEG.tobytes()

            new_frames = False
            # print('Frame captured')
    cap.release()

record_thread = threading.Thread(target=record)
record_thread.daemon = True


if __name__ =='__main__':
    record_thread.start()
    while True: # since record_thread is a daemon, main thread must be kept alive
        if not new_frames:
            pass