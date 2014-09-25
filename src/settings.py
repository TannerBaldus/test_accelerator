import re
import makefile_templates as makefiles
##################################################
# Helper Functions for Building Framework Parsers
##################################################
def c_class(text):
    """
    Isolates class name for c_lang family.
    :param text: text to be searched
    :return: class name if there is a match, None Otherwise
    """
    if re.search(r'class', text):
        return  re.sub(r'[-(<: ].*', '', re.sub(r'.*class(. ?)', '', text))
    return None

def replace(regex, replacement,text):
    """
    Takes a piece of text and 
    """
    substitute = re.sub(regex, replacement, text)
    if substitute != text:
        return substitute
    return None

def boost_test_case(text):
    if re.search('BOOST_AUTO_TEST_CASE'):
        return text[text.find("(")+1:text.find(")")].strip()
    return  None

##################################################
# Framework Parser Definitions
##################################################
NUnit = {
    'nodes': [
        {'depth': 0, 'initial': lambda text: replace(r'namespace(. ?)', '',text)},
        {'depth': 1, 'initial': lambda text: re.search('\[TestFixture.*\]', text),
         'after': lambda text: c_class(text)}
    ],
    'command': '/run={suite} /nologo {test_file}',
    'strip': True,
    'makefile': makefiles.gnu,
}

Boost = {
    'nodes':[
        {'depth': 0,  'initial': lambda text: boost_test_case(text)}
    ],
    'command': ('{test_file} --run-test={test} --log_format=XML --log_level=all --report_level=no'
                '--log_sink={test_file}_{suite}.x64d.xml'),
    'makefile': makefiles.boost,
    'strip': True,
}





#####################################################
# Add Framework Name: Framework Definition Pairs Here
#####################################################
INSTALLED_FRAMEWORKS = {'NUnit': NUnit, 'Boost': Boost}


#####################################################
# Getters
#####################################################
class SettingsError(Exception):
    pass

def get_framework(in_framework):
    """
    Handles getting the framework from the INSTALLED_FRAMEWORKS. Raises Exception if
    the framework is missing
    :param arguments: argparse arguments
    :return: framework dict
    """
    framework = INSTALLED_FRAMEWORKS.get(in_framework)
    if not framework:
        raise SettingsError('{} not in  INSTALLED_FRAMEWORKS check settings.py'.format(in_framework))
    return framework


def get_component(framework, in_component):
    """
    Gets a desired component from a framework dict. Raises an exception if not defined.
    :param framework:name of framework dict
    :param in_component: desired component name
    :return: the value of the component
    """
    framework = get_framework(framework)
    component = framework.get(in_component)
    if not component:
        raise SettingsError("{} not defined in settings for {}".format(in_component, framework))
    return component


