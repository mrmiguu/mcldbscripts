from time import sleep
from pyautogui import press
from argparse import ArgumentParser
import threading
from pynput import mouse

default_start = 1
default_interval_secs = 5
default_countdown_secs = 10

interrupt_event = threading.Event()


def programmatically_carousel_through_slide_range(
    start: int, end: int, interval_secs: int
):
    slide = start

    while not interrupt_event.is_set():
        press(f"{slide}")
        press("enter")

        interrupt_event.wait(interval_secs)

        slide = slide % end + 1

    # jump to the slide just after the end of the carousel
    press(f"{end+1}")
    press("enter")


def on_click(x, y, button, pressed):
    if not pressed:
        print("You interrupted the robot!!")
        interrupt_event.set()
        return False


if __name__ == "__main__":
    parser = ArgumentParser(
        description="A submissive robot that turns a range of your slides into a slideshow"
    )
    parser.add_argument(
        "-s", "--start", type=int, help="The starting slide number of the slideshow"
    )
    parser.add_argument(
        "-e",
        "--end",
        type=str,
        help="The ending slide number of the slideshow before it loops around",
    )
    parser.add_argument(
        "-i", "--interval", type=str, help="The number of seconds inbetween slides"
    )
    parser.add_argument(
        "-c",
        "--countdown",
        type=str,
        help="The number of seconds the robot will countdown to until starting",
    )

    args = parser.parse_args()

    if not args.end:
        raise Exception("You forgot to specify an --end slide number for the slideshow")

    start = int(args.start) if args.start else default_start
    end = int(args.end)
    interval_secs = int(args.interval) if args.interval else default_interval_secs
    countdown_secs = int(args.countdown) if args.countdown else default_countdown_secs

    if start:
        print("Slideshow starting slide:", start)
    if end:
        print("Slideshow ending slide:", end)
    if interval_secs:
        print("Slideshow interval (seconds):", interval_secs)
    if countdown_secs:
        print("Slideshow countdown (seconds):", countdown_secs)

    print("----------------------------------------------------------------")
    print("Click your mouse anywhere to interrupt the slideshow robot")
    print(
        "Move your mouse to the upper-left corner of your screen to immediately short circuit the slideshow robot"
    )
    print("----------------------------------------------------------------")

    print(
        f"You have {countdown_secs} seconds to do what you need to do before the robot starts automatically..."
    )
    sleep(1)
    for s in reversed(range(countdown_secs)):
        print(f"You have {s} seconds...")
        sleep(1)

    print(f"The robot has started!")

    mouse_listener = mouse.Listener(on_click=on_click)
    mouse_listener.start()

    try:
        programmatically_carousel_through_slide_range(
            start=start,
            end=end,
            interval_secs=interval_secs,
        )
    finally:
        mouse_listener.join()

    print(f"The robot has stopped")
