from flogin import PlainTextCondition, RegexCondition, KeywordCondition, MultiCondition, Query
import pytest, re

@pytest.fixture
def yes_query():
    return Query(raw_text="bar foo", text="foo", keyword="bar")

@pytest.fixture
def no_query():
    return Query(raw_text="car foo", text="apple", keyword="car")

conditions = {
    "PlainTextCondition": PlainTextCondition("foo"),
    "RegexCondition": RegexCondition(re.compile(r"^[foo]*$")),
    "KeywordCondition-Allowed": KeywordCondition(allowed_keywords="bar"),
    "KeywordCondition-Disallowed": KeywordCondition(disallowed_keywords="car"),
    "MultiCondition": MultiCondition(
        [PlainTextCondition("foo"), RegexCondition(re.compile(r"[foo]*"))]
    )
}

@pytest.fixture(params=conditions.values(), ids=list(conditions.keys()))
def condition(request):
    return request.param

def test_conditions_1(condition, yes_query: Query):
    res = condition(yes_query)
    assert res == True

def test_conditions_2(condition, no_query: Query):
    res = condition(no_query)
    assert res == False