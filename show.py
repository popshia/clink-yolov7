import argparse

import cv2

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="show source")
    opts = parser.parse_args()

    if opts.source.split(".")[1] in ["jpg", "png", "bmp"]:
        img = cv2.imread(opts.source)
        print(type(img), img.shape)
        cv2.imshow("img", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        cap = cv2.VideoCapture(opts.source)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Can't receive frame. Exiting ...")
                break
            cv2.imshow("video", frame)
            if cv2.waitKey(1) > -1:
                break
