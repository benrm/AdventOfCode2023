
import re

map_name_re = re.compile("([\w-]+) map:")

class Range:
    def __init__(self, origin, length):
        self.origin = origin
        self.length = length

    def __lt__(self, other):
        return self.origin + self.length < other.origin

    def __eq__(self, other):
        return self.origin == other.origin and self.length == other.length

    def __str__(self):
        return f"Range(origin={self.origin};range={self.length})"

    def __repr__(self):
        return self.__str__()

    def copy(self):
        return Range(self.origin, self.length)

def map_range_to(_range_maps, _ranges):
    maps = sorted(_range_maps)
    ranges = sorted(_ranges)
    ret = []
    while len(maps) > 0 and len(ranges) > 0:
        if ranges[0].origin < maps[0].src.origin:
            _range = ranges.pop(0)
            if _range.origin+_range.length < maps[0].src.origin:
                ret.append(_range)
            elif _range.origin+_range.length == maps[0].src.origin:
                pass
            elif _range.origin+_range.length > maps[0].src.origin:
                length = maps[0].src.origin - _range.origin
                ret.append(Range(_range.origin, length))
                ranges.insert(0, Range(maps[0].src.origin, maps[0].src.length - length))
            else:
                raise Exception("Unreachable branch")
        elif ranges[0].origin == maps[0].src.origin:
            _range = ranges.pop(0)
            _map = maps.pop(0)
            if _range.length < _map.length:
                length = _map.length - _range.length
                ret.append(Range(map_to(_range_maps, _range.origin), length))

            elif _range.length == _map.length:
                pass
            elif _range.length > _map.length:
                pass
            else:
                raise Exception("Unreachable branch")
        elif ranges[0].origin > maps[0].src.origin:
            if ranges[0].origin+ranges[0].length < maps[0].src.origin:
                pass
            elif ranges[0].origin+ranges[0].length == maps[0].src.origin:
                pass
            elif ranges[0].origin+ranges[0].length > maps[0].src.origin:
                pass
            else:
                raise Exception("Unreachable branch")
        else:
            raise Exception("Unreachable branch")
    if len(ranges) > 0:
        ret.extend(ranges)
    return ret

class RangeMap:
    def __init__(self, dst, src, length):
        self.dst = Range(dst, length)
        self.src = Range(src, length)

    def __lt__(self, other):
        return self.src.__lt__(other.src)

    def __str__(self):
        return f"RangeMap(dst={self.dst},src={self.src})"

    def __repr__(self):
        return self.__str__()

def map_to(_range_maps, _id):
    for _range in _range_maps:
        if _range.src.origin <= _id and _id < _range.src.origin+_range.src.length:
            return _id - _range.src.origin + _range.dst.origin
    return _id

def parse(lines):
    ret = {}
    i = 0
    while i < len(lines):
        while i < len(lines):
            if lines[i].strip():
                break
            i += 1

        matches = map_name_re.match(lines[i])
        if not matches:
            raise Exception(f"Line did not match map format: {lines[i]}")
        name = matches[1]
        i += 1

        maps = []
        while i < len(lines):
            if not lines[i].strip():
                break
            maps.append(RangeMap(*[ int(word) for word in lines[i].split() ]))
            i += 1
        ret[name] = maps

    return ret
