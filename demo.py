import logging
import os
import sys
from datetime import datetime
from subprocess import PIPE, Popen

import wget

SUPPORT_MODEL = ["v7", "tiny"]

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


class WrongModelError(Exception):
    def __init__(self, message):
        super().__init__(message)


class VidNotExistError(Exception):
    def __init__(self, message):
        super().__init__(message)


class DoubleCheckDeclineError(Exception):
    def __init__(self, message):
        super().__init__(message)


class CalledProcessError(Exception):
    def __init__(self, message):
        super().__init__(message)


def SetupLogger():
    file_handler = logging.FileHandler(
        "logs/{}.log".format(datetime.today().strftime("%Y-%m-%d_%H:%M"))
    )
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        datefmt="%Y-%m-%d_%H:%M",
        handlers=[file_handler, console_handler],
    )
    logging.getLogger("requests").setLevel(logging.NOTSET)


def CheckModel(chosen_model):
    if chosen_model == 0 or chosen_model > len(SUPPORT_MODEL):
        logging.warning("\nWRONG MODEL TYPE, PLEASE SELECT AGAIN!")


def CheckVideo(args):
    if not os.path.isfile(args.video):
        raise VidNotExistError(
            "'{}' doesn't exist, please check the file path.".format(args.video)
        )


def DoubleCheck(args):
    proceed = input(
        """
Please review your arguments:

1. Chosen model: {}
2. Given demo video: {}

Proceed? (y/n) """.format(
            args.model, args.video
        )
    )
    if proceed != "y":
        raise DoubleCheckDeclineError(
            "Please run the demo script with the your preferred arguments again."
        )


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
    else:
        return "./weights/yolov7.pt"


def RunInference(args):
    weight = ModelArgToWeight(args.model)
    command = (
        "python detect.py --weights {} --conf 0.25 --imgsize 640 --source {}".format(
            weight, args.video
        )
    )
    logging.info("running command: {}".format(command))
    process = Popen(command, stdout=PIPE)
    while True:
        stdout = process.stdout.readline().rstrip().decode("utf-8")
        if process.poll() != 0:
            raise CalledProcessError(
                "Inference process error, please contact the maintainer!"
            )
        elif stdout:
            logging.info(stdout.strip())
        else:
            break


if __name__ == "__main__":
    SetupLogger()
    logging.info(SCRIPT_TITLE)

    while True:
        logging.info("\n-------------- Support Models --------------")
        for i, model in enumerate(SUPPORT_MODEL):
            logging.info("{}: {} \t\t".format(i + 1, model))

        while True:
            model = int(input("\nPlease choose the model you wish to use: "))
            if CheckModel(model) == False:
                break

            video = input("\nPlease enter the path of the file you wish to inference: ")

            while True:
                if CheckVideo(video) == False:


    # try:
    #     DoubleCheck(args)
    #     CheckModel(args)
    #     CheckVideo(args)
    #     RunInference(args)
    # except Exception as e:
    #     logging.info("\n")
    #     logging.info(e)
    #     if type(e).__name__ not in [
    #         WrongModelError,
    #         VidNotExistError,
    #         DoubleCheckDeclineError,
    #         CalledProcessError,
    #     ]:
    #         logging.info(
    #             "\nInference process error, please contact the maintainer!"
    #         )
    # finally:
    #     break
