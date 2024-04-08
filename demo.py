import os
import sys
import time
from datetime import datetime
from subprocess import Popen

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


def PrintSupportModel():
    print("\n-------------------- Support Models ---------------------")
    for i, model in enumerate(sorted(os.listdir("./weights/"))):
        print("{}: {} \t\t".format(i + 1, model))
    print("---------------------------------------------------------")


def PrintVideos():
    print("\n------------------- Available Videos --------------------")
    for i, video in enumerate(sorted(os.listdir("./videos/"))):
        print("{}: {} \t\t".format(i + 1, video))
    print("---------------------------------------------------------")
    print(
        """
* if you can't find your video down below,
  please press 'q' to exit and transfer the video again! """
    )


def CheckModel(model_index):
    if model_index == 0 or model_index > len(os.listdir("./weights/")):
        print("WRONG MODEL TYPE, PLEASE SELECT AGAIN!")
        time.sleep(0.5)
        return False

    print("Model selected: {}\n".format(model))
    return sorted(os.listdir("./weights/"))[model_index - 1]


def CheckVideo(video_index):
    if video_index == "q":
        exit(0)
    if video_index == "0" or int(video_index) > len(os.listdir("./videos/")):
        print("WRONG VIDEO INDEX, PLEASE SELECT AGAIN!")
        time.sleep(0.5)
        return False

    print("Video selected: {}\n".format(video))
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
        print("PLEASE STARTOVER AGAIN!")
        time.sleep(0.5)
        os.execl(sys.executable, sys.executable, *sys.argv)


def RunInference(model, video):
    model = os.path.join("./weights/", model)
    video = os.path.join("./videos/", video)
    command = [
        "python",
        "detect.py",
        "--conf",
        "0.25",
        "--img-size",
        "640",
        "--weights",
        model,
        "--source",
        video,
        "--name",
        datetime.today().strftime("%Y%m%d_%H%M"),
    ]
    print("\nRunning Inference...\n")
    process = Popen(command).wait()
    exit(0)


if __name__ == "__main__":
    print(SCRIPT_TITLE)

    while True:
        PrintSupportModel()

        while True:
            model = int(input("\nPlease select model: "))
            model = CheckModel(model)
            if model == False:
                break

            while True:
                PrintVideos()

                while True:
                    video = input("\nPlease select video or 'q' to exit: ")
                    video = CheckVideo(video)
                    if video == False:
                        break

                    DoubleCheck(model, video)

                    try:
                        RunInference(model, video)
                    except Exception as e:
                        print(e)
                        print(
                            "\nInference process error, please contact the script maintainer!"
                        )
                        exit(0)
