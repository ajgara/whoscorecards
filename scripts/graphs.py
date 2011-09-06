import math
from processutils import numutils, xmlutils

class LineGraph(object):
    def __init__(self, line_id, min_height=285.5, max_height=223):
        self.line_id = line_id
        self.min_height = min_height
        self.max_height = max_height
        self.values = {}
        self.ticks = None

    def add_value(self, year, value):
        self.values[int(year)] = value


    @property
    def max_tick(self):
        num_ticks = len(self.ticks)
        return self.ticks[num_ticks]

    @property
    def pixel_range(self):
        return abs(self.max_height - self.min_height)

    def update_points(self, xml, reverse=False):
        node = xmlutils.get_el_by_id(xml, "polyline", self.line_id)
        coords = node.attributes["points"].value
        coords = [tpl.split(",") for tpl in coords.split()]
        if reverse: coords = coords[::-1]
        new_coords = []
        for year, (x, y) in zip(range(2002, 2010), coords):
            y = self.min_height - self.values[year] / self.max_tick * self.pixel_range 
            print year, y, self.values[year]
            new_coords.append((x, y))
        node.attributes["points"].value = " ".join("%s,%s" % (x, y) for (x, y) in new_coords)

    def update_values(self, xml, ids):
        for year in range(2002, 2010):
            node = xmlutils.get_el_by_id(xml, "text", ids[year])
            height = self.min_height - self.values[year] / self.max_tick * self.pixel_range
            print year, height, self.values[year]
            node.setAttribute("y", str(height - 6))


class BarGraph(object):
    def __init__(self, tick_multiplier=1.2, num_ticks=6, min_height=285.5, max_height=223):
        self.values = {}
        self.max_height = max_height
        self.min_height = min_height
        self.num_ticks = num_ticks
        self.tick_multiplier = tick_multiplier

    def add_value(self, year, value):
        self.values[int(year)] = value

    @property
    def ticks(self):
        high = max(self.values.values())
        top = numutils.condround(high * self.tick_multiplier)
        ticksz = top / (self.num_ticks - 1)
        return { tick + 1 : ticksz * tick for tick in range(self.num_ticks) }

    @property
    def max_tick(self):
        return self.ticks[self.num_ticks]

    @property
    def pixel_range(self):
        return abs(self.max_height - self.min_height)

    def update_bars(self, xml, ids):
        for year in range(2002, 2010):
            node = xmlutils.get_el_by_id(xml, "path", ids[year])
            d = node.attributes["d"].value.split()
            d[2] = "V"
            d[3] = str(self.min_height - self.values[year] / self.max_tick * self.pixel_range)
            node.attributes["d"].value = " ".join(d)

    def update_values(self, xml, ids):
        for year in range(2002, 2010):
            node = xmlutils.get_el_by_id(xml, "text", ids[year])
            height = self.min_height - self.values[year] / self.max_tick * self.pixel_range
            node.setAttribute("y", str(height - 6))

class RectBarGraph(BarGraph):
    def __init__(self, tick_multiplier=1.2, num_ticks=6, min_height=285.5, max_height=223, max_tick=None):
        self._max_tick = max_tick
        super(RectBarGraph, self).__init__(tick_multiplier, num_ticks, min_height, max_height)

    @property
    def max_tick(self):
        return self._max_tick or super(RectBarGraph, self).max_tick

    def update_bars(self, xml, ids):
        #import pdb; pdb.set_trace()
        for year in range(2002, 2010):
            node = xmlutils.get_el_by_id(xml, "rect", ids[year])
            y = self.min_height -  self.values[year] / self.max_tick * self.pixel_range
            height = self.min_height - y
            node.setAttribute("y", str(y))
            node.setAttribute("height", str(height))

class PieChart(object):
    def __init__(self, xml, centre, radius, data, colours=None):
        self.xml = xml
        self.centre = centre
        self.radius = radius
        self.data = data
        if colours == None:
            self.colours = ["#cf3d96", "#62a73b", "#79317f", "#009983"]
        else:
            self.colours = colours

    def generate_xml(self):
        total = sum(self.data)
        if total == 0: return

        centre_x, centre_y = self.centre
        percs = [v / total for v in self.data]

        prev_angle = 0
        for perc in percs:
            new_angle = prev_angle + 2 * math.pi * perc
            segment = {
                "centre_x" : centre_x,
                "centre_y" : centre_y,
                "start_x" : centre_x - math.cos(prev_angle) * self.radius,
                "start_y" : centre_y - math.sin(prev_angle) * self.radius,
                "end_x" : centre_x - math.cos(new_angle) * self.radius,
                "end_y" : centre_y - math.sin(new_angle) * self.radius,
                "long_arc" : 1 if perc > 0.5 else 0,
                "radius" : self.radius,
            } 
            self.generate_segment(segment)
            prev_angle = new_angle

    def generate_segment(self, segment):
        colour = self.colours[0]
        self.colours = self.colours[1:] + [colour]
        root = self.xml.documentElement
        segment_node = self.xml.createElement("path")
        path_d="M%(centre_x)f,%(centre_y)f L%(start_x)f,%(start_y)f A%(radius)f, %(radius)f 0 %(long_arc)d,1 %(end_x)f,%(end_y)f Z" % segment
        segment_node.setAttribute("d", path_d)
        segment_node.setAttribute("stoke", "black")
        segment_node.setAttribute("stoke-width", "2")
        segment_node.setAttribute("style", "fill:%s" % colour)
        root.appendChild(segment_node)
