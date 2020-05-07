from imutils.video import FileVideoStream
from imutils.video import FPS
import argparse
import imutils
import time
import mtcnn
import cv2
import os
import numpy as np
from pathlib import Path

#from utils import VideoMeta
from tf_pose.networks import get_graph_path

from tf_pose.estimator import TfPoseEstimator


class PoseExtract:
    cv2_base_dir = os.path.dirname(os.path.abspath(cv2.__file__))
    haar_model = os.path.join(cv2_base_dir, 'data/haarcascade_frontalface_default.xml')
    face_cascade = cv2.CascadeClassifier(haar_model)
    cwd = os.getcwd()
    face_cascade.load(haar_model)
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

    # construct the argument parse and parse the arguments
    def argument_parser(self):
        args = argparse.ArgumentParser()
        args.add_argument("-v", "--video", required=True,
                          help="path to input video file")
        args.add_argument("--output-dir", default="video_output",
                          help="path to output files")
        args.add_argument("--select-frame", default="video_output",
                          help="path to output files")
        args.add_argument("--detect", default="haarcascade", help="choose the model to detect faces")
        return args.parse_args()

    def crop(self, image_obj, shape, saved_location):
        x, y, w, h = shape
        box = (y, y + h, x, x + w)
        if sum(n < 0 for n in box) == 0:
            cv2.imwrite(saved_location, image_obj[box[0]:box[1], box[2]:box[3]])
        else:
            cv2.imwrite(saved_location, image_obj)

    def read_frames(self):
        # start the file video stream thread and allow the buffer to
        # start to fill
        print("[INFO] starting video file thread...")
        args = self.argument_parser()
        output_path = self.cwd / Path(args.output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        fvs = FileVideoStream(args.video).start()
        time.sleep(1.0)

        # start the FPS timer
        fps = FPS().start()
        detector = mtcnn.MTCNN()
        fno = 0
        #frames = VideoMeta(args.video).fps()
        #print(meta)
        e = TfPoseEstimator(get_graph_path("mobilenet_thin"), target_size=(432, 368))
        # loop over frames from the video file stream
        while fvs.more():
            fno += 1
            print(fno)
            # grab the frame from the threaded video file stream, resize
            # it, and convert it to grayscale (while still retaining 3
            # channels)
            frame = fvs.read()
            #if (fno % frames != 0):
             #   continue
            try:
                frame = imutils.resize(frame, width=432,height=368)
            except:
                break
            #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            #frame = np.dstack([frame, frame, frame])

            humans = e.inference(frame)
            image = TfPoseEstimator.draw_humans(frame, humans, imgcopy=False)
            print("humans:",humans)

            # display the size of the queue on the frame
            # cv2.putText(frame, "Queue Size: {}".format(fvs.Q.qsize()),
            #            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            # show the frame and update the FPS counter
            cv2.imshow("Frame", image)
            cv2.waitKey(1)
            fps.update()

        # stop the timer and display FPS information
        fps.stop()
        print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

        # do a bit of cleanup
        cv2.destroyAllWindows()
        fvs.stop()


if __name__ == "__main__":
    face_extract = PoseExtract()
    face_extract.argument_parser()
    face_extract.read_frames()
