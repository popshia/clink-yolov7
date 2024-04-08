import logging
import os
import sys
import time
from datetime import datetime
from subprocess import PIPE, Popen

import wget

SUPPORT_MODEL = ["v7", "tiny", "vehicle", "hualian-port"]

SCRIPT_TITLE = """
         __ _         __                     __             _____
  _____ / /(_)____   / /__    __  __ ____   / /____  _   __/__  /
 / ___// // // __ \\ / //_/   / / / // __ \\ / // __ \\| | / /  / /
/ /__ / // // / / // ,<     / /_/ // /_/ // // /_/ /| |/ /  / /
\\___//_//_//_/ /_//_/|_|    \\__, / \\____//_/ \\____/ |___/  /_/
       __                  /____/
  ____/ /___   ____ ___   ____
 / __  // _ \\ / __ `__ \\ / __ \\
/ /_/ //  __// / / / / // /_/ /
\\__,_/ \\___//_/ /_/ /_/ \\____/
"""


class CalledProcessError(Exception):
    def __init__(self, message):
        super().__init__(message)


def SetupLogger():
    file_handler = logging.FileHandler(
        "logs/{}.log".format(datetime.today().strftime("%Y%m%d_%H%M"))
    )
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        datefmt="%Y%m%d_%H%M",
        handlers=[file_handler, console_handler],
    )
    logging.getLogger("requests").setLevel(logging.NOTSET)


def PrintSupportModel():
    logging.info("\n-------------------- Support Models ---------------------")
    for i, model in enumerate(SUPPORT_MODEL):
        logging.info("{}: {} \t\t".format(i + 1, model))
    logging.info("---------------------------------------------------------")


def PrintVideos():
    logging.info("\n------------------- Available Videos --------------------")
    for i, video in enumerate(sorted(os.listdir("./videos/"))):
        logging.info("{}: {} \t\t".format(i + 1, video))
    logging.info("---------------------------------------------------------")
    logging.info(
        """
* if you can't find your video down below,
  please press 'q' to exit and transfer the video again! """
    )


def CheckModel(model_index):
    if model_index == 0 or model_index > len(SUPPORT_MODEL):
        logging.warning("WRONG MODEL TYPE, PLEASE SELECT AGAIN!")
        time.sleep(0.5)
        return False

    return SUPPORT_MODEL[model_index - 1]


def CheckVideo(video_index):
    if video_index == "q":
        exit(0)
    if video_index == "0" or int(video_index) > len(os.listdir("./videos/")):
        logging.warning("WRONG VIDEO INDEX, PLEASE SELECT AGAIN!")
        time.sleep(0.5)
        return False

    return sorted(os.listdir("./videos/"))[int(video_index) - 1]


def DoubleCheck(model, video):
    proceed = input(
        """
Please review your selections:

1. Chosen model: {}
2. Chosen video: {}

Proceed? (y/n) """.format(
            model, video
        )
    )
    if proceed != "y":
        logging.warning("PLEASE STARTOVER AGAIN!")
        time.sleep(0.5)
        os.execl(sys.executable, sys.executable, *sys.argv)


def ModelArgToWeight(model):
    if model == "v7":
        url = "https://github.com/WongKinYiu/yolov7/releases/download/v0.1/yolov7.pt"
        if os.path.isfile("./weights/yolov7.pt"):
            return "./weights/yolov7.pt"
        else:
            logging.info("\nDownloading yolov7.pt from github...")
            return wget.download(url, out="weights")
    elif model == "tiny":
        url = (
            "https://github.com/WongKinYiu/yolov7/releases/download/v0.1/yolov7-tiny.pt"
        )
        if os.path.isfile("./weights/yolov7-tiny.pt"):
            return "./weights/yolov7-tiny.pt"
        else:
            logging.info("\nDownloading yolov7-tiny.pt from github...")
            return wget.download(url, out="weights")
    elif model == "vehicle":
        return "./weights/vehicle.pt"
    elif model == "hualian-port":
        return "./weights/hualian_port_0329.pt"


def RunInference(model, video):
    weight = ModelArgToWeight(model)
    command = (
        "python detect.py --weights {} --conf 0.25 --imgsize 640 --source {}".format(
            weight, video
        )
    )
    process = Popen(command, stdout=PIPE)
    while True:
        stdout = process.stdout.readline().rstrip().decode("utf-8")
        if process.poll() == 0:
            break
        elif stdout:
            logging.info(stdout.strip())
        else:
            break


if __name__ == "__main__":
    SetupLogger()
    logging.info(SCRIPT_TITLE)

    while True:
        PrintSupportModel()

        while True:
            model = int(input("\nPlease select model: "))
            model = CheckModel(model)
            if model == False:
                break

            logging.info("Model selected: {}\n".format(model))

            while True:
                PrintVideos()

                while True:
                    video = input("\nPlease select video or 'q' to exit: ")
                    video = CheckVideo(video)
                    if video == False:
                        break

                    logging.info("Video selected: {}\n".format(video))
                    DoubleCheck(model, video)
                    logging.info("\nRunning Inference...\n")

                    try:
                        RunInference(model, video)
                    except Exception as e:
                        print(e)
                        logging.warning(
                            "\nInference process error, please contact the maintainer!"
                        )
                        exit(0)
