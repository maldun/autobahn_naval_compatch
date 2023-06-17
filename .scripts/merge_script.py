# -*- coding: utf-8 -*-
from Hoi4Converter.parser import parse_grammar as code2obj
from Hoi4Converter.converter import *
from Hoi4Converter.mappings import *
import Hoi4Converter
import os
import sys
import pandas as pd
import shutil
HOME = os.path.expanduser("~/")
sys.path.append(HOME + "prog/Python/hoi4_converter/")

HOI4_FOLDER = HOME + ".local/share/Steam/steamapps/common/Hearts of Iron IV/"
KR_FOLDER = HOME + ".local/share/Steam/steamapps/workshop/content/394360/1521695605/"
KX_FOLDER = HOME + ".local/share/Steam/steamapps/workshop/content/394360/2076426030/"
# RT56_FOLDER = HOME + ".local/share/Steam/steamapps/workshop/content/394360/820260968/"
RT56_FOLDER = HOME + ".local/share/Paradox Interactive/Hearts of Iron IV/mod/1956_beta/"
KR_NAVAL_FOLDER = HOME + \
    ".local/share/Steam/steamapps/workshop/content/394360/2862849828/"
KX_NAVAL_FOLDER = HOME + \
    ".local/share/Steam/steamapps/workshop/content/394360/2964793578/"

# Set for mod in question
KX = True

KR_OUT_FOLDER = HOME + \
    ".local/share/Paradox Interactive/Hearts of Iron IV/mod/autobahn_naval_compatch"
KX_OUT_FOLDER = HOME + \
    ".local/share/Paradox Interactive/Hearts of Iron IV/mod/autobahn_kx_naval_compatch"
OUT_FOLDER = KX_OUT_FOLDER if KX is True else KR_OUT_FOLDER
NAVAL_FOLDER = KX_NAVAL_FOLDER if KX is True else KR_NAVAL_FOLDER

IDEA_PATH = "common/ideas"
INTERFACE_PATH = "interface"
SCRIPTED_EFFECTS_PATH = "common/scripted_effects"
HISTORY_COUNTRY_PATH = "history/countries"
DECISION_PATH = "common/decisions"
# RULES_PATH =

TECH_TREE_GUI = "countrytechtreeview.gui"
NAVAL_KEY = "naval_folder"
MTG_KEY = "mtgnavalfolder"


def read_gui(fname):
    with open(fname, "r") as f:
        code = f.read()
        code = code.replace('%%', '%')
        obj = code2obj(code)

    return obj


def get_replacement_index(obj, key):
    searcher = code2obj(f'name = "{key}"')[0]
    found = has_key_and_val.search(obj, searcher)
    index = found[1][0][-3]
    return index


def replace_segment(org, new, key):
    index = get_replacement_index(new, key)
    new_obj = new[0][1][1][1][index]
    index_org = get_replacement_index(org, key)
    org[0][1][1][1][index_org] = new_obj
    return org


def merge_techtree():
    os.makedirs(os.path.join(OUT_FOLDER, INTERFACE_PATH), exist_ok=True)
    rt56_tt_fname = os.path.join(RT56_FOLDER, INTERFACE_PATH, TECH_TREE_GUI)
    krnr_tt_fname = os.path.join(NAVAL_FOLDER, INTERFACE_PATH, TECH_TREE_GUI)

    rt56_tt = read_gui(rt56_tt_fname)
    krnr_tt = read_gui(krnr_tt_fname)

    new_obj = replace_segment(rt56_tt, krnr_tt, NAVAL_KEY)
    new_obj = replace_segment(new_obj, krnr_tt, MTG_KEY)
    with open(os.path.join(OUT_FOLDER, INTERFACE_PATH, TECH_TREE_GUI), 'w') as fp:
        code = list2paradox(new_obj).replace("%", "%%")
        fp.write(code)


if __name__ == "__main__":
    merge_techtree()
