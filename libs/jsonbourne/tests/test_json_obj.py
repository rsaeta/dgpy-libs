# -*- coding: utf-8 -*-
# =============================================================================
#  (c) Copyright 2020, Dynamic Graphics, Inc.
#  ALL RIGHTS RESERVED
#  Permission to use, copy, modify, or distribute this software for any
#  purpose is prohibited without specific, written prior permission from
#  Dynamic Graphics, Inc.
# =============================================================================
"""Python builtin data structure utils"""

from decimal import Decimal

import pytest

from jsonbourne import JSON, JsonObj


pytestmark = [pytest.mark.basic]


class Thingy(JsonObj):
    @property
    def herm(self):
        return "hermproperty"


def test_dictainer_basic() -> None:
    thing = Thingy({"a": 1, "b": 2, "c": 3})
    assert thing.a == thing["a"]

    thing2 = Thingy({"a": 1, "b": 2, "c": {"herm": 23}})
    assert thing2.c.herm == thing2["c"]["herm"]


def test_dictainer_basic_unpacking() -> None:
    thing = Thingy({"a": 1, "b": 2, "c": 3, "d": ["list"]})
    thing2 = Thingy({"a": 1, "b": 2, "c": 3, "d": ["different list"], "a": 234})
    assert thing.a == thing["a"]

    for e in thing:
        print(e)
    for e in thing.items():
        print(e)
    print({**thing})
    assert {**thing} == {"a": 1, "b": 2, "c": 3, "d": ["list"]}
    assert {**thing2} == {"a": 234, "b": 2, "c": 3, "d": ["different list"]}

    merged = {**thing, **thing2}
    assert merged["a"] == 234
    merged_dictainer = JsonObj({**thing, **thing2})
    assert {**merged_dictainer} == merged


def test_dictainer_breaks() -> None:
    thing2 = Thingy({"a": 1, "b": 2, "c": {"herm": 23}})
    assert thing2.c.herm == thing2["c"]["herm"]
    with pytest.raises(ValueError) as err:
        thing2["herm herm herm import"] = "should break"


class ThingyWithMethod(JsonObj):
    def a_property(self) -> str:
        return "prop_value"


def test_dictainer_method() -> None:
    thing_w_prop = ThingyWithMethod({"a": 1, "b": 2, "c": {"herm": 23}})
    assert thing_w_prop.c.herm == thing_w_prop["c"]["herm"]
    assert thing_w_prop.a_property() == "prop_value"
    assert thing_w_prop["a_property"]() == "prop_value"


def test_dictainer_method_set_attr() -> None:
    thing_w_prop = ThingyWithMethod({"a": 1, "b": 2, "c": {"herm": 23}})
    assert thing_w_prop.c.herm == thing_w_prop["c"]["herm"]
    assert thing_w_prop.a_property() == "prop_value"
    assert thing_w_prop["a_property"]() == "prop_value"
    thing_w_prop.some_attr = "attr_value"
    assert thing_w_prop.some_attr == "attr_value"
    assert thing_w_prop["some_attr"] == "attr_value"
    assert hasattr(thing_w_prop, "some_attr")


class ThingyWithProperty(JsonObj):
    @property
    def a_property(self) -> str:
        return "prop_value"


def test_dictainer_property() -> None:
    thing_w_prop = ThingyWithProperty(
        **{"a": 1, "b": 2, "c": {"herm": 23}, "d": {"nested": "nestedval"}}
    )
    assert thing_w_prop.c.herm == thing_w_prop["c"]["herm"]
    assert thing_w_prop.a_property == "prop_value"
    assert thing_w_prop["a_property"] == "prop_value"
    assert thing_w_prop.d.nested == "nestedval"
    # with pytest.raises(ValueError) as err:
    #     thing2['herm herm herm import'] = 'should break'


def test_protected_attrs_slash_members():
    j = JsonObj()
    j.key = 'value'
    j['12'] = 'twelve'
    print(j.__dict__)
    print(j.items)
    with pytest.raises(ValueError):
        j.items = [1, 2, 3, 4]
    j['items'] = [1, 2, 3, 4]
    print(j.__dict__)
    print(j)
    j_items = j.items
    print('items', j_items)
    assert j.items != [1, 2, 3, 4]
    assert j['items'] == [1, 2, 3, 4]


def test_number_keys():
    j = JsonObj()
    j.key = 'value'
    j['12'] = 'twelve'
    assert j['12'] == 'twelve'


data = {
    "id": 1,
    "code": None,
    "subd": {"a": 23, "b": {"herm": 2}},
    "type": "foo",
    "root": {
        "string_list": ['one', 'two', 'octopus', 'what_is_up'],
        "mixed_dict": {"num": 123, "obj": {"k": "v"}, "list": ['s', 123, {'k': 'v'}]},
    },
    "bars": [
        {"id": 6934900},
        {"id": 6934977},
        {"id": 6934992},
        {"id": 6934993},
        {"id": 6935014},
    ],
    "n": 10,
    "date_str": "2013-07-08 00:00:00",
    "float_here": 0.454545,
    "complex": [{"id": 83865, "goal": Decimal("2.000000"), "state": "active"}],
    "profile_id": None,
    "state": "active",
}


def test_dot_items():
    jd: JsonObj = JSON(data)
    print(jd.dot_keys_list())
    expected = [
        ('id', 1),
        ('code', None),
        ('subd.a', 23),
        ('subd.b.herm', 2),
        ('type', 'foo'),
        ('root.string_list', ['one', 'two', 'octopus', 'what_is_up']),
        ('root.mixed_dict.num', 123),
        ('root.mixed_dict.obj.k', 'v'),
        ('root.mixed_dict.list', ['s', 123, JsonObj(**{'k': 'v'})]),
        (
            'bars',
            [
                JsonObj(**{'id': 6934900}),
                JsonObj(**{'id': 6934977}),
                JsonObj(**{'id': 6934992}),
                JsonObj(**{'id': 6934993}),
                JsonObj(**{'id': 6935014}),
            ],
        ),
        ('n', 10),
        ('date_str', '2013-07-08 00:00:00'),
        ('float_here', 0.454545),
        (
            'complex',
            [JsonObj(**{'id': 83865, 'goal': Decimal('2.000000'), 'state': 'active'})],
        ),
        ('profile_id', None),
        ('state', 'active'),
    ]
    from pprint import pprint

    pprint(jd.dot_items_list())
    dkl = jd.dot_items_list()
    assert expected == dkl

    # from time import time
    # ta = time()
    # # for i in range(10):
    # for i in range(100):
    #     a = list(jd.dot_items_chain())
    # tb = time()
    # for i in range(100):
    #     b = list(jd.dot_items_chain2())
    # tc = time()
    # for i in range(100):
    #     c = list(jd.dot_items())
    # td = time()
    # print('yielding', tc-tb,'-- chain: ', tb-ta, '-- og: ', td-tc)
    expected_json_str = JSON.stringify(expected, sort_keys=True, pretty=True)
    output_json_str = JSON.stringify(dkl, sort_keys=True, pretty=True)
    assert output_json_str == expected_json_str
    try:
        from deepdiff import DeepDiff

        print('deepdiff', DeepDiff(expected, dkl))
        assert not DeepDiff(expected, dkl)
    except ModuleNotFoundError as mnfe:
        print(mnfe)


d1 = {
    "id": 1,
    "code": None,
    "subd": {"a": 23, "b": {"herm": 2}},
    "type": "foo",
    "bars": [
        {"id": 6934900},
        {"id": 6934977},
        {"id": 6934992},
        {"id": 6934993},
        {"id": 6935014},
    ],
    "n": 10,
    "date_str": "2013-07-08 00:00:00",
    "float_here": 0.454545,
    "complex": [{"id": 83865, "goal": Decimal("2.000000"), "state": "active"}],
    "profile_id": None,
    "state": "active",
}

d2 = {
    "id": "2",
    "code": None,
    "type": "foo",
    "bars": [
        {"id": 6934900},
        {"id": 6934977},
        {"id": 6934992},
        {"id": 6934993},
        {"id": 6935014},
    ],
    "n": 10,
    "date_str": "2013-07-08 00:00:00",
    "float_here": 0.454545,
    "complex": [{"id": 83865, "goal": Decimal("2.000000"), "state": "active"}],
    "profile_id": None,
    "state": "active",
}


def test_dotlookup() -> None:
    d = JsonObj(d1)
    dot_get = d.subd.a
    dot_lookup = d["subd.a"]
    assert dot_lookup == dot_get


def test_dotlookup_no_dots() -> None:
    d = JsonObj(d1)
    dot_get = d.n
    dot_lookup = d.dot_lookup("n")
    assert dot_lookup == dot_get


def test_dotlookup_dont_exist() -> None:
    d = JsonObj(d1)
    with pytest.raises(KeyError):
        dot_lookup = d["subd.a.hermhermherm.ohno"]


def test_dot_iter_keys() -> None:
    d = JsonObj(d1)
    expected = [
        "id",
        "code",
        "subd.a",
        "subd.b.herm",
        "type",
        "bars",
        "n",
        "date_str",
        "float_here",
        "complex",
        "profile_id",
        "state",
    ]
    assert expected == list(d.dot_keys())


def test_dot_list_keys() -> None:
    d = JsonObj(d1)
    expected = [
        "id",
        "code",
        "subd.a",
        "subd.b.herm",
        "type",
        "bars",
        "n",
        "date_str",
        "float_here",
        "complex",
        "profile_id",
        "state",
    ]
    assert set(expected) == set(d.dot_keys_list())


def test_dot_list_keys_sorted() -> None:
    d = JsonObj(d1)
    expected = [
        "id",
        "code",
        "subd.a",
        "subd.b.herm",
        "type",
        "bars",
        "n",
        "date_str",
        "float_here",
        "complex",
        "profile_id",
        "state",
    ]
    assert sorted(expected) == d.dot_keys_list(sort_keys=True)


def test_json_dict_reject_non_string_key():
    t1 = {1: None, 2: 2}
    with pytest.raises(ValueError):
        jd = JsonObj(t1)


def test_filter_none():
    t1 = {
        "falsey_dict": {},
        "falsey_list": [],
        "falsey_string": "",
        "is_false": False,
        "a": None,
        "b": 2,
        "c": {
            "d": "herm",
            "e": None,
            "falsey_dict": {},
            "falsey_list": [],
            "falsey_string": "",
            "is_false": False,
        },
    }
    result = JsonObj(t1).filter_none()
    print(JsonObj(t1).filter_none())
    assert result == JsonObj(
        **{
            "falsey_dict": {},
            "falsey_list": [],
            "falsey_string": "",
            "is_false": False,
            "b": 2,
            "c": {
                "d": "herm",
                "e": None,
                "falsey_dict": {},
                "falsey_list": [],
                "falsey_string": "",
                "is_false": False,
            },
        }
    )


def test_filter_none_recursive():
    t1 = {
        "falsey_dict": {},
        "falsey_list": [],
        "falsey_string": "",
        "is_false": False,
        "a": None,
        "b": 2,
        "c": {
            "d": "herm",
            "e": None,
            "falsey_dict": {},
            "falsey_list": [],
            "falsey_string": "",
            "is_false": False,
        },
    }
    result = JsonObj(t1).filter_none(recursive=True)
    print(result)
    assert result == JsonObj(
        **{
            "falsey_dict": {},
            "falsey_list": [],
            "falsey_string": "",
            "is_false": False,
            "b": 2,
            "c": {
                "d": "herm",
                "falsey_dict": {},
                "falsey_list": [],
                "falsey_string": "",
                "is_false": False,
            },
        }
    )


def test_filter_false():
    t1 = {
        "falsey_dict": {},
        "falsey_list": [],
        "falsey_string": "",
        "is_false": False,
        "a": None,
        "b": 2,
        "c": {
            "d": "herm",
            "e": None,
            "falsey_dict": {},
            "falsey_list": [],
            "falsey_string": "",
            "is_false": False,
        },
    }
    result = JsonObj(t1).filter_false()
    assert result == JsonObj(
        **{
            "b": 2,
            "c": {
                "d": "herm",
                "e": None,
                "falsey_dict": {},
                "falsey_list": [],
                "falsey_string": "",
                "is_false": False,
            },
        }
    )


def test_filter_falsey_recursive():
    d = {
        "falsey_dict": {},
        "falsey_list": [],
        "falsey_string": "",
        "is_false": False,
        "a": None,
        "b": 2,
        "c": {
            "d": "herm",
            "e": None,
            "falsey_dict": {},
            "falsey_list": [],
            "falsey_string": "",
            "is_false": False,
        },
    }
    result = JsonObj(d).filter_false(recursive=True)
    assert result == JsonObj(**{"b": 2, "c": {"d": "herm"}})
