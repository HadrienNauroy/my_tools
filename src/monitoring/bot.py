"""This script is aimed too define all useful function for monitoring another bot with messenger"""

from message import *
import time as tm
from enum import Enum
from enum import unique


@unique
class State(Enum):
    r"""
    The diffrent possible state of Monitor_Bot:
        - trading
        - stand_by
    """

    trading = 1
    stand_by = 2


class MessageError(Exception):
    def __init__(self, type, world):
        self.message = (
            f"'{world}' is not recognised as a {type}, ignoring this command."
        )


class Monitor_Bot:
    r"""
    A type of bot that is able to send messages and retreive instruction from user

    Accepted command :
        - START : start the other bot for undefined time
        - START for <duration> : start the other bot for <duration>
        - STOP : stop the other bot for undefined time
        - STOP for <duration> : stop the other bot for <duration>

        Note that "Stop" or "stop" will also work

    Accepted duration :
        - "x s" /  "x sec" / "x second" / "x seconds" / "x secs"
        - "x m" / "x min" / "x mins" / "x minute" / "x minutes"
        - "x h" / "x hour" / "x hours
        - "x d" / "x day" / "x day"

        Note that a space is required between x and the time frame

    Usage exemple:
        - in messenger : "STOP for 1 hour"
        - in messenger : "START

    Any other command will Raise an Error wich will be sended to user on messenger


    """

    # better if this is common to all instance of this class, avoid use of RAM
    browser = connect()

    def __init__(self):
        tm.sleep(0.5)
        self.state = State.trading
        self.last_message = retreive_messages(self.browser)
        print(self.last_message)
        self.trading_duration = None
        self.stand_by_duration = None

    def _update_state(self):
        messages = retreive_messages(self.browser)

        # if nothing has changed
        if messages == [] or messages == self.last_message:
            return False

        for message in messages:
            worlds = message.split()
            try:

                # to avaoid infinite loop of message error
                if worlds[0][0] == "'":
                    pass

                # to avoid detecting what we sent
                elif worlds[0] in ["Entrer", "Vous", "En", "Now", "Bot", "Absolut"]:
                    pass

                # STOP command handling
                elif worlds[0] in ["STOP", "Stop", "stop"]:
                    self.state = State.stand_by
                    if len(worlds) == 1:
                        self.stand_by_duration = None

                    elif len(worlds) == 4:
                        time_frame = worlds[3]
                        try:
                            duration = float(worlds[2])
                        except Exception as e:
                            raise MessageError("duration", worlds[2])

                        if time_frame in ["s", "sec", "second", "seconds", "secs"]:
                            multiplyer = 1
                        elif time_frame in ["m", "min", "mins", "minute", "minutes"]:
                            multiplyer = 60
                        elif time_frame in ["h", "hours", "hour"]:
                            multiplyer = 3_600
                        elif time_frame in ["day", "d", "days"]:
                            multiplyer = 3_600 * 24
                        else:
                            raise MessageError("time frame", worlds[3])
                        self.stand_by_duration = duration * multiplyer

                    else:
                        raise MessageError("command", message)

                # START command handling
                elif worlds[0] in ["START", "Start", "start"]:
                    self.state = State.trading
                    if len(worlds) == 1:
                        self.trading_duration = None

                    elif len(worlds) == 4:
                        time_frame = worlds[3]
                        try:
                            duration = float(worlds[2])
                        except Exception as e:
                            raise MessageError("duration", worlds[2])

                        if time_frame in ["s", "sec", "second", "seconds", "secs"]:
                            multiplyer = 1
                        elif time_frame in ["m", "min", "mins", "minute", "minutes"]:
                            multiplyer = 60
                        elif time_frame in ["h", "hours", "hour"]:
                            multiplyer = 3_600
                        elif time_frame in ["day", "d", "days"]:
                            multiplyer = 3_600 * 24
                        else:
                            raise MessageError("time frame", worlds[3])
                        self.trading_duration = duration * multiplyer

                    else:
                        raise MessageError("command", message)

                else:
                    raise MessageError("command", message)

            except MessageError as e:
                send_message(self.browser, e.message)

        self.last_message = messages
        self.last_updtate = tm.time()
        return True

    def monitor(self):
        r"""
        The main function that returns True if the bot we are monitoring should trade
        and False otherwise.

        This is the function one should call in an other script to monitor something.
        """

        self._update_state()

        if self.state == State.trading:

            if self.trading_duration == None:
                return True
            elif self.trading_duration > tm.time() - self.last_updtate:
                return True
            else:
                return False

        if self.state == State.stand_by:
            return False


if __name__ == "__main__":
    bot = Monitor_Bot()
    try:
        while True:
            bot.update_state()
            print(
                f"State: {bot.state}, durations: {bot.stand_by_duration}/{bot.trading_duration}\r",
                end="",
            )

    except KeyboardInterrupt:
        bot.browser.close()
