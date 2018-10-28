class Quadruples:
    def __init__(self):
        # list of quadruple (each represented by list of string of *maximum* length 4)
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
        quads.insert(next_quad, quad) # TODO, don't we just append it to the end ...
        self.next_quad += 1 # TODO, why don't we use increment_quad, HMMMM

    def print(self):
        print("CODE")
        num_quads = len(self.quads)
        for i in range(1, num_quads):
            quad = self.quads[i]
            out = str(i) + ": " + quad[0]

            # TODO: is it okay to assume, that four will values will always be set counting nulls?
            if quad[1]:
                out += " " + quad[1]
            if quad[2]:
                out += ", " + quad[2]
            if quad[3]:
                out += ", " + quad[3]

            print(out)