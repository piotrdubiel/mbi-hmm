from nose.tools import raises
from schema import SchemaError
import hmm_decoder

@raises(SystemExit)
def string_window_test():
    # Given
    arguments = {'<window_length>': 'not_a_number'}

    # When
    hmm_decoder.validate(arguments)

@raises(SystemExit)
def negative_window_test():
    # Given
    arguments = {'<window_length>': 2}

    # When
    hmm_decoder.validate(arguments)
