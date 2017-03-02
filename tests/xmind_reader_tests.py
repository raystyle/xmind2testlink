from src.xmind_reader import *
from os import path
import logging

xml_path = path.join(path.dirname(__file__), 'xmind_content.xml')
root_node = read_xml_as_etree(xml_path)


def test_parse_step():
    step_node = root_node.find('.//topic[@id="2t8lod6ibp7b5cruhn5mle90vi"]')
    step = parse_step(step_node)
    assert isinstance(step, TestStep)
    assert step.number == 1
    assert step.action == "step 1"
    assert step.expected == "expected 1"

    # no expected node
    step_node = root_node.find('.//topic[@id="6tjmi45cj0dcfnanvplp6ug1u3"]')
    step = parse_step(step_node)
    assert isinstance(step, TestStep)
    assert step.number == 1
    assert step.action == "step 1 action without expected"
    assert step.expected == ""


def test_parse_steps():
    testcase_node = root_node.find('.//topic[@id="6utjnqagpc7cg6p85gk3i2qjhb"]')
    steps_node = children_topics_of(testcase_node)
    steps = parse_steps(steps_node)
    logging.info(steps)
    assert len(steps) == 2
    assert steps[0].number == 1
    assert steps[0].action == 'step 1'
    assert steps[1].number == 2
    assert steps[1].expected == 'expected 2'


def test_parse_testcase():
    testcase_node = root_node.find('.//topic[@id="6utjnqagpc7cg6p85gk3i2qjhb"]')
    testcase = parse_testcase(testcase_node)
    assert isinstance(testcase, TestCase)
    assert testcase.name == 'test case 1'
    assert testcase.steps[0].action == 'step 1'
    assert testcase.importance == 1
    assert testcase.summary == "summary"
    assert testcase.preconditions == ""


def test_parse_suite():
    suite_node = root_node.find('.//topic[@id="5t69j48tjorm60fq4og9l82t06"]')
    suite = parse_suite(suite_node)
    assert isinstance(suite, TestSuite)
    assert suite.name == 'apple suite'
    assert len(suite.testcase_list) == 3
    assert suite.testcase_list[0].name == 'test case title for apple 1'
    assert suite.details == "this will be a detail or summary note"


def test_parse_xmind_content():
    test_suite = parse_xmind_content(xml_path)
    assert isinstance(test_suite, TestSuite)
    assert test_suite.name == ""
    assert len(test_suite.sub_suites) == 5
    assert test_suite.sub_suites[0].name == "demo suite"