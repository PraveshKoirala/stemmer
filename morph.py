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
        tokens = open(self.suffix_rule_file_name, "r").decode("utf-8").split("\n")
        for rules, suffix in zip(tokens[::2], tokens[1::2]):
            num, type, subrule, morph, desc, ignore = rules.split(" ")
            # num is the rule number
            self.suffix_rules[num] = dict(type=type, subrule=subrule, morph=morph, desc=desc, ignore=ignore)
            if type == "SFX":
                pass
            else:
                pass

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

