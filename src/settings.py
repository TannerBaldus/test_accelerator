import re
from makefile_templates import GNUMAKE_TEMPLATE

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


replace = lambda text, substitute: substitute if substitute != text else None

def match_string(pattern, text):
    match = re.search(pattern, text)
    if match:
        return match.string
    return None



##################################################
# Framework Parser Definitions
##################################################
nunit = {'command': '/run={suite} /nologo {test_file}',
         'strip': True,
         'makefile': GNUMAKE_TEMPLATE,
         'nodes': [
             {'depth': 0, 'initial': lambda text: replace(text, re.sub(r'namespace(. ?)', '', text))},
             {'depth': 1, 'initial': lambda text: re.search('\[TestFixture.*\]', text),
              'after': lambda text: c_class(text)}
         ]
         }





#####################################################
# Add Framework Name: Framework Definition Pairs Here
#####################################################
INSTALLED_FRAMEWORKS = {'nunit': nunit}

