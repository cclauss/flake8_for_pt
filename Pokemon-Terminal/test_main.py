#!/usr/bin/env python3

# To run the tests, use: python3 -m pytest --capture=sys

from collections import namedtuple
from database import Database
from main import main

region_record = namedtuple('region_record', 'roman_number start end')
region_dict = {
    "kanto": region_record("I", 1, 151),
    "johto": region_record("II", 152, 251),
    "hoenn": region_record("III", 252, 386),
    "sinnoh": region_record("IV", 387, 493),
    "extra": region_record("", 494, 100000)
}

db = Database()
print(len(db))
print(len(db.get_kanto()))
print(len(db.get_johto()))
print(len(db.get_hoenn()))
print(len(db.get_sinnoh()))
print(len(db.get_extra()))


def test_no_args(capsys):
    with pytest.raises(SystemExit):
        main([__file__])
    out, err = capsys.readouterr()
    assert out.startswith("No command line arguments specified.")


def test_len():
    # Database unfortunately makes db.__MAX_ID private :-(
    __MAX_ID = 493
    assert len(db) == __MAX_ID + len(db.get_extra())


def _test_region(region_name):
    region_name = (region_name or 'extra').lower()
    # Database unfortunately makes db.__get_region() private :-(
    func = {
        "kanto": db.get_kanto,
        "johto": db.get_johto,
        "hoenn": db.get_hoenn,
        "sinnoh": db.get_sinnoh,
        "extra": db.get_extra
    }[region_name]
    pokemon_list = func()
    region_record = region_dict[region_name]
    start = region_record.start
    end = len(db) if region_name == "extra" else region_record.end
    # make sure there are no missing pokemon
    assert len(pokemon_list) == end - start + 1
    if region_name == "extra":
        return
    # make sure that all pokemon.id are in the ID range
    assert all([start <= int(p.get_id()) <= end for p in pokemon_list])


def test_regions():
    for region_name in region_dict:
        _test_region(region_name)


def test_three_args(capsys):
    main([__file__, 1, 2, 3])
    out, err = capsys.readouterr()
    assert out.startswith("Invalid number of arguments.")
