class Quadruples:
    def __init__(self):
        # list of quadruples, each represented by list of four string
        # the default element is placeholder, because we are counting from 1...
        self.quads = [[None, None, None, None]]
        self.next_quad = 1

    def get_field(self, quad_idx, idx):
        return self.quads[quad_idx][idx]

    def set_field(self, quad_idx, idx, field):
        self.quads[quad_idx][idx] = field

    def get_next_quad(self):
        return self.next_quad

    def increment_quad(self):
        self.next_quad += 1

    def get_quad(self, idx):
        return self.quads[idx]

    def add_quad(self, quad):
        self.quads.insert(self.next_quad, quad)
        self.increment_quad()

    def print(self):
        print("CODE")
        num_quads = len(self.quads)
        for i in range(1, num_quads):
            quad = self.quads[i]
            out = str(i) + ": " + quad[0]

            if quad[1]:
                out += " " + str(quad[1])
            if quad[2]:
                out += ", " + str(quad[2])
            if quad[3]:
                out += ", " + str(quad[3])

            print(out)