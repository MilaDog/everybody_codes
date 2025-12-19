# Advent of Code
# MilaDog

import math as _math
from enum import Enum
from typing import Union


class TimingSymbols(Enum):
    """
    TimingSymbols Symbols used for representing timing values
    """

    SECONDS = "s"
    MILLISECONDS = "ms"
    MICROSECONDS = "µs"
    NANOSECONDS = "ns"

    def __eq__(self, other):
        """Comparing enumeration values"""
        if isinstance(other, str):
            return self.value == other

        if isinstance(other, Enum):
            return self.value == other.value

        return False


class Timing:
    def __init__(self, seconds: Union[int, float] = 0):
        # Converting seconds into desired outputs
        seconds_frac, s = _math.modf(seconds)
        self._seconds_raw = seconds
        self._milliseconds_raw = seconds * 1000
        self._microseconds_raw = seconds * 1e6
        self._nanoseconds_raw = seconds * 1e9

        _, ms = _math.modf(seconds_frac * 1000)
        _, us = _math.modf(seconds_frac * 1e6)
        _, ns = _math.modf(seconds_frac * 1e9)

        self._seconds = int(s)
        self._milliseconds = int(ms)
        self._microseconds = int(us)
        self._nanoseconds = int(ns)

    def __str__(self):
        """Get the string representation of the object"""
        s: str = (
            "seconds=%d; milliseconds=%02d; microseconds=%02d; nanoseconds= %02d"
            % (
                self._seconds,
                self._milliseconds,
                self._microseconds,
                self._nanoseconds,
            )
        )
        return s

    def result(self):
        return "{:.5f}".format(self._seconds_raw) + "s"

    @property
    def seconds(self):
        """Get seconds value"""
        return self._seconds

    @property
    def milliseconds(self):
        """Get milliseconds value"""
        return self._milliseconds

    @property
    def microseconds(self):
        """Get microseconds value"""
        return self._microseconds

    @property
    def nanoseconds(self):
        """Get nanoseconds value"""
        return self._nanoseconds

    @property
    def seconds_raw(self):
        """Get seconds raw value"""
        return self._seconds_raw

    @property
    def milliseconds_raw(self):
        """Get milliseconds raw value"""
        return self._milliseconds_raw

    @property
    def microseconds_raw(self):
        """Get microseconds raw value"""
        return self._microseconds_raw

    @property
    def nanoseconds_raw(self):
        """Get nanoseconds raw value"""
        return self._nanoseconds_raw
