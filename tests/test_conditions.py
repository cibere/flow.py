from flogin import PlainTextCondition, RegexCondition, KeywordCondition, MultiCondition, Query
import pytest, re

@pytest.fixture
def yes_query():
    return Query(raw_text="bar foo", text="foo", keyword="bar")

@pytest.fixture
def no_query():
    return Query(raw_text="car foo", text="apple", keyword="car")

@pytest.fixture(params=[0, 1])
def query(yes_query: Query, no_query: Query, request: pytest.FixtureRequest):
    return [yes_query, no_query][request.param]

conditions = {
    "PlainTextCondition": PlainTextCondition("foo"),
    "RegexCondition": RegexCondition(re.compile(r"^[foo]*$")),
    "KeywordCondition-Allowed": KeywordCondition(allowed_keywords="bar"),
    "KeywordCondition-Disallowed": KeywordCondition(disallowed_keywords="car"),
    "CustomCondition": lambda q: q.text == "foo"
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

multi_condition_both_tests = [
    MultiCondition(
        conditions['PlainTextCondition'],
        conditions['RegexCondition'],
    ),
    MultiCondition(
        conditions['KeywordCondition-Allowed'],
        conditions['CustomCondition'],
    ),
    MultiCondition(
        conditions['KeywordCondition-Allowed'],
        conditions['KeywordCondition-Disallowed'],
    ),
    MultiCondition(
        conditions['KeywordCondition-Disallowed'],
        conditions['RegexCondition'],
    )
]
multi_condition_mismatch_tests = [
    MultiCondition(
        cond,
        lambda q: q.text == "bar",
    )
    for cond in conditions.values()
]

class TestMultiCondition:
    @pytest.fixture(scope="class", params=multi_condition_both_tests)
    def both_mul_cond(self, request: pytest.FixtureRequest):
        return request.param
    
    @pytest.fixture(scope="class", params=multi_condition_mismatch_tests)
    def mismatch_mul_cond(self, request: pytest.FixtureRequest):
        return request.param

    def test_multicondition_1(self, both_mul_cond: MultiCondition, yes_query: Query):
        res = both_mul_cond(yes_query)
        assert res == True
    
    def test_multicondition_2(self, both_mul_cond: MultiCondition, no_query: Query):
        res = both_mul_cond(no_query)
        assert res == False
    
    def test_multicondition_3(self, mismatch_mul_cond: MultiCondition, query: Query):
        res = mismatch_mul_cond(query)
        assert res == False