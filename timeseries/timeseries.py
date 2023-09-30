#!/usr/bin/python

import unittest
import math

from typing import List

nan = float('nan')


class Point:
    def __init__(self, val, ts):
        self.val = val
        self.ts = ts

    def __repr__(self):
        return "(ts=%s, val=%s)" % (self.ts, self.val)

class TestFix(unittest.TestCase):

    def test_1_passthrough(self):
        """test_passthrough validates that fix returns the inp data if no modifications are required."""

        inp = [
          Point(0, 100),
          Point(8.4, 110),
          Point(0.999, 120),
        ]
        got = fix(inp, 100, 130, 10)
        exp = [
          Point(0, 100),
          Point(8.4, 110),
          Point(0.999, 120),
        ]

        self.assert_result(inp, exp, got)

    def test_2_apply_from_to(self):
        """test_apply_from_to validates that fix only returns points that lie within the from/to range provided."""

        inp = [
          Point(0.5, 100),
          Point(8.4, 110),
          Point(32.5, 120),
          Point(0.999, 130),
        ]
        got = fix(inp, 110, 130, 10)
        exp = [
          Point(8.4, 110),
          Point(32.5, 120),
        ]

        self.assert_result(inp, exp, got)

    def test_3_apply_from_to_nans(self):
        """test_apply_from_to_nans validates that fix adds NaNs at the front or end as needed to match the requested range."""

        inp = [
          Point(0.5, 100),
          Point(41.3, 110),
        ]
        got = fix(inp, 90, 140, 10)
        exp = [
          Point(nan, 90),
          Point(0.5, 100),
          Point(41.3, 110),
          Point(nan, 120),
          Point(nan, 130),
        ]

        self.assert_result(inp, exp, got)

    def test_4_apply_irregular_from_to_nans(self):
        """test_apply_irregular_from_to_nans validates that fix honors from/to even when they are irregular (when they are not divisible by the interval)."""

        inp = [
          Point(0.5, 100),
          Point(41.3, 110),
        ]
        got = fix(inp, 89, 131, 10)
        exp = [
          Point(nan, 90),
          Point(0.5, 100),
          Point(41.3, 110),
          Point(nan, 120),
          Point(nan, 130),
        ]

        self.assert_result(inp, exp, got)

    def test_5_adjust_irregular_timestamps(self):
        """test_adjust_irregular_timestamps validates that fix adjusts timestamps to be divisible by the interval."""

        inp = [
          Point(0.5, 100),
          Point(8.4, 110),
          Point(32.5, 118),
          Point(0.999, 130),
          Point(41.3, 139),
          Point(41.9, 141),
        ]
        got = fix(inp, 100, 160, 10)
        exp = [
          Point(0.5, 100),
          Point(8.4, 110),
          Point(32.5, 120),
          Point(0.999, 130),
          Point(41.3, 140),
          Point(41.9, 150),
        ]

        self.assert_result(inp, exp, got)

    def test_6_insert_nans(self):
        """test_insert_nans validates that fix inserts NaNs for missing points."""

        inp = [
          Point(0.5, 100),
          Point(32.5, 120),
          Point(0.999, 130),
          Point(41.3, 150),
        ]
        got = fix(inp, 100, 160, 10)
        exp = [
          Point(0.5, 100),
          Point(nan, 110),
          Point(32.5, 120),
          Point(0.999, 130),
          Point(nan, 140),
          Point(41.3, 150),
        ]

        self.assert_result(inp, exp, got)

    def test_7_filter_duplicates(self):
        """test_filter_duplicates validates that fix filters out points that correspond to the same output timestamp."""
        inp = [
          Point(0.5, 100),
          Point(0.7, 100),
          Point(32.5, 110),
          Point(0.9, 120),
          Point(0.8, 125),
          Point(41.3, 130),
          Point(41.3, 140),
          Point(41.2, 141),
          Point(41.3, 142),
          Point(41.4, 149),
        ]
        got = fix(inp, 100, 160, 10)
        exp = [
          Point(0.5, 100),
          Point(32.5, 110),
          Point(0.9, 120),
          Point(0.8, 130),
          Point(41.3, 140),
          Point(41.2, 150),
        ]

        self.assert_result(inp, exp, got)

    def test_8_irregular_from_to_irregular_timestamps(self):
        """
        test_irregular_from_to_irregular_timestamps validates that fix correctly handles the combination
        of irregular from/to parameters with irregular inp timestamps (irregular meaning not divisible by interval).
        Note that the from/to filtering should be applied to the adjusted timestamps.
        """

        inp = [
          Point(0.5, 105),
          Point(1, 120),
          Point(1.5, 130),
          Point(2, 135),
          Point(3, 139),
        ]
        got = fix(inp, 108, 138, 10)
        exp = [
          Point(0.5, 110),
          Point(1, 120),
          Point(1.5, 130),
        ]

        self.assert_result(inp, exp, got)

    def test_9_all_at_once(self):
        """test_all_at_once validates that fix can handle all the above conditions all at once."""

        inp = [
          Point(0.5, 105),
          Point(41.3, 111),
          Point(0, 130),
          Point(1, 150),
          Point(2, 151),
          Point(3, 152),
          Point(4, 159),
          Point(4, 160),
          Point(5, 160),
          Point(4, 174),
          Point(5, 175),
          Point(6, 185),
        ]
        got = fix(inp, 81, 186, 10)
        exp = [
          Point(nan, 90),
          Point(nan, 100),
          Point(0.5, 110),
          Point(41.3, 120),
          Point(0, 130),
          Point(nan, 140),
          Point(1, 150),
          Point(2, 160),
          Point(nan, 170),
          Point(4, 180),
        ]

        self.assert_result(inp, exp, got)

    def assert_result(self, inp, exp, got):
        message = "Output mismatch\nInput:\n{}\nExpected:\n{}\nGot:\n{}\n".format(inp, exp, got)
        self.assertTrue(self.equal(exp, got), message)

    def equal(self, exp, got):
        if len(exp) != len(got):
            return False
        for pgot, pexp in zip(got, exp):
            if math.isnan(pgot.val) != math.isnan(pexp.val):
                return False

            if not math.isnan(pgot.val) and pgot.val != pexp.val:
                return False

            if pgot.ts != pexp.ts:
                return False

        return True

def fix( inp:List[Point], start:int, end:int, interval:int) -> List[Point]:

    out:List[Point] = []

    # generator produces a paced stream
    # we will remove inp elements accordingto the generated time ticks
    start1 = interval * (start // interval)
    if start1 < start:
      start1 += interval

    cursor = start1
    index_inp = 0
    inp_len = len( inp )
    while cursor < end:
      pnt = None
      if index_inp < inp_len:
        point_inp = inp[ index_inp ]
        if point_inp.ts == cursor:
          pnt = point_inp
          index_inp += 1

        elif point_inp.ts < cursor:
          index_inp += 1
          if cursor - point_inp.ts < interval:
            pnt = Point( point_inp.val, cursor )
          else:
            continue

      if pnt is None:
        pnt = Point( nan, cursor )

      out.append( pnt )
      cursor += interval

    return out


if __name__ == '__main__':
    unittest.main()
