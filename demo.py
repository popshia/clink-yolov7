import argparse
import os
from subprocess import PIPE, Popen


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


def CheckModel(args):
    supported_model = ["car", "people"]
    if args.model not in supported_model:
        raise WrongModelError(
            "'{}' isn't a valid model type, please select from: ['', ''].".format(
                args.model
            ),
        )


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
    if model == "car":
        return "./weights/yolov7.pt"
    elif model == "boat":
        return "./weights/yolov7.pt"
    else:
        return "./weights/yolov7.pt"


def RunInference(args):
    weight = ModelArgToWeight(args.model)
    command = (
        "python detect.py --weights {} --conf 0.25 --imgsize 640 --source {}".format(
            weight, args.video
        )
    )
    process = Popen(command, stdout=PIPE)
    while True:
        stdout = process.stdout.readline().rstrip().decode("utf-8")
        if process.poll() != 0:
            raise CalledProcessError(
                "Inference process error, please contact the maintainer!"
            )
        elif stdout:
            print(stdout.strip())
        else:
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="This is a demo script using yolov7 as its backend."
    )
    parser.add_argument("--model", type=str, help='model type: ["", ""]')
    parser.add_argument("--video", type=str, help="demo video to be inferenced")
    args = parser.parse_args()

    while 1:
        try:
            DoubleCheck(args)
            CheckModel(args)
            CheckVideo(args)
            RunInference(args)
        except Exception as e:
            print("\n", end="")
            print(e)
            if type(e).__name__ not in [
                WrongModelError,
                VidNotExistError,
                DoubleCheckDeclineError,
                CalledProcessError,
            ]:
                print("\nInference process error, please contact the maintainer!")
        finally:
            break
