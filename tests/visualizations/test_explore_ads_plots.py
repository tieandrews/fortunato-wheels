# Author: Ty Andrews
# Date: 2023-05-08
import os, sys
import pytest
   
# ensure that the parent directory is on the path for relative imports
SRC_PATH = sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)

from src.visualizations.explore_ads_plots import hex_to_rgba


# test that hex_to_rgba returns the correct rgba color code
def test_hex_to_rgba():
    # test that hex_to_rgba returns the correct rgba color code
    assert hex_to_rgba("#ffffff") == "rgba(255,255,255,1.00)"
    assert hex_to_rgba("#000000") == "rgba(0,0,0,1.00)"
    assert hex_to_rgba("#ff0000") == "rgba(255,0,0,1.00)"
    assert hex_to_rgba("#00ff00") == "rgba(0,255,0,1.00)"
    assert hex_to_rgba("#0000ff") == "rgba(0,0,255,1.00)"
    assert hex_to_rgba("#ffff00") == "rgba(255,255,0,1.00)"
    assert hex_to_rgba("#00ffff") == "rgba(0,255,255,1.00)"
    assert hex_to_rgba("#ff00ff") == "rgba(255,0,255,1.00)"

def test_hex_to_rgba_opacity():
    # test that hex_to_rgba returns the correct rgba color code with opacity
    assert hex_to_rgba("#ffffff", opacity=0.5) == "rgba(255,255,255,0.50)"
    assert hex_to_rgba("#000000", opacity=0.5) == "rgba(0,0,0,0.50)"
    assert hex_to_rgba("#ff0000", opacity=0.5) == "rgba(255,0,0,0.50)"
    assert hex_to_rgba("#00ff00", opacity=0.5) == "rgba(0,255,0,0.50)"
    assert hex_to_rgba("#0000ff", opacity=0.5) == "rgba(0,0,255,0.50)"
    assert hex_to_rgba("#ffff00", opacity=0.5) == "rgba(255,255,0,0.50)"
    assert hex_to_rgba("#00ffff", opacity=0.5) == "rgba(0,255,255,0.50)"
    assert hex_to_rgba("#ff00ff", opacity=0.5) == "rgba(255,0,255,0.50)"
