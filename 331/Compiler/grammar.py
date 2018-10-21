class Grammar:
    def __init__(self, grammar_file, table_file):
        self.terms = {}
        self.non_terms = {}
        self.grammar = self.create_grammar(grammar_file)
        self.table = self.create_table(table_file)

    def create_grammar(self, file):
        grammar_file = open(file, 'r')
        grammar_str = grammar_file.read()

        grammar = [["PLACEHOLDER"]]  # grammar rules start from index 1
        for line in grammar_str.splitlines():
            right_hand = line.split("::=")[1][1:]  # 1: ignore extra first space
            right_hand_list = []
            for unit in right_hand.split(' '):
                if unit and unit[0] != '<': # capitalize non-terminals
                    unit = unit.upper()

                right_hand_list.append(unit)

            # remove excess and wild ''
            if len(right_hand_list) > 1 and right_hand_list[-1] == '':
                right_hand_list = right_hand_list[:-1]

            grammar.append(right_hand_list)

        return grammar

    def create_table(self, file):
        table_file = open(file, 'r')
        table_str = table_file.read()

        term_vals = []
        table = []
        for line in table_str.splitlines()[1:]:
            term_vals.append(line.split(",")[0])
            table.append(line.split(",")[1:])

        i = 0
        for term_val in term_vals:
            self.terms[term_val.upper()] = i  # assume all uppercase
            i += 1

        i = 0
        for non_term in table_str.splitlines()[0].split(",")[1:]:
            self.non_terms[non_term] = i
            i += 1

        return table

    def prod_num(self, term, non_term):
        return int(self.table[self.terms[term]][self.non_terms[non_term]])

    def prod(self, prod_num):
        return self.grammar[prod_num]

    def is_non_term(self, label):
        return label in self.non_terms

    def is_action(self, label):
        return label and label[0] == '#' # not empty and starts with pound sign
