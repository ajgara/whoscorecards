import math

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
