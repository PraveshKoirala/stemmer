# coding=utf-8
from __future__ import unicode_literals
__author__ = 'pravesh'


class Morph:

    def read_root_list(self):
        for word in open(self.root_file_name, "r").decode("utf-8").split("\n"):
            # some of the words have pos information .. e.g. अखानो|NN, some are in the form र|CCON|N
            tokens = word.split("|")
            pos, suffix = "", ""
            if len(tokens) <= 2:
                root, pos = tokens
            else:
                root, pos, suffix = tokens
            self.roots.append(root)
            self.pos[root] = pos or None
            self.root_suffix[root] = suffix or None

    def read_suffix_list(self):
        """
        Suffixes are of the form
        एका|11
        where एका is the suffix and 11 is the rule number
        :return:
        """
        for word in open(self.suffix_file_name, "r").decode("utf-8").split("\n"):
            suffix, rule = word.split("|")
            self.suffixes.append(suffix)
            self.suffix_rules[suffix] = rule

    def read_suffix_rule(self):
        """
        The suffix rule is of the following form
        RN  SFX(X)  sub-rules   morph   morph-tag   ignore

        RN: The rule number
        SFX(X): The type of the rule, either SFX or SFXX, not sure what they do yet
        sub-rules: The number of sub-rules, determines the number of following lines
        morph:  The actual suffix e.g. आइ, एको etc
        morph-tag:  The english tag of morph i.e. AAI, EKO etc
        ignore: Whether to ignore in second parse, not sure what they do yet.
        :return:
        """
        tokens = open(self.suffix_rule_file_name, "r").decode("utf-8").split("\n")
        # Remove all empty lines.
        tokens = filter(None, tokens)
        while tokens:
            rule = tokens.pop(0)
            num, type, subrule, morph, tag, ignore = rule.split(" ")
            num, subrule = int(num), int(subrule)
            self.suffix_rules[num] = dict(type=type, subrule=subrule, morph=morph, tag=tag, ignore=ignore,
                                          strip_rule=[])
            strip_rule = []
            # now the sub-rules
            for i in range(subrule):
                line = tokens.pop(0)
                # regular suffix
                if type == "SFX":
                    delete, insert = line.split(" ")
                    strip_rule.append(dict(insert=insert.replace(".", ""), delete=delete))
                # irregular suffix
                elif type == "SFXX":
                    # todo irregular suffix here
                    pass

            # sort the strip rule according to the length of what to delete
            if "delete" in strip_rule[0]:
                sorted(strip_rule, key=lambda sub_rule: len(sub_rule["delete"]))
            self.suffix_rules[num].strip_rule=strip_rule

    def __init__(self, root_file_name, suffix_file_name, suffix_rule_file_name):
        """

        :param root_file_name: root file name
        :return:
        """
        # list of available roots
        self.suffix_rule_file_name = suffix_rule_file_name
        self.roots = []
        # mapping from root -> pos if exist, else root -> None
        self.pos = {}
        # mapping from root -> suffix if exist, else root -> None. I don't understand it either
        self.root_suffix = {}

        self.root_file_name = root_file_name
        # read root
        self.read_root_list()

        # SKIPPED THE ALT ROOT
        # Read the suffix list and rules
        self.suffixes = []
        self.suffix_rules = {}
        self.suffix_file_name = suffix_file_name
        self.read_suffix_list()
        self.read_suffix_rule()

