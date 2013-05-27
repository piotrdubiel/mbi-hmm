from nose.tools import raises
from schema import SchemaError
import hmm_generator

@raises(SystemExit)
def validate_test():
    # Given
    arguments = {'<fasta_sequence>': 'non_existing_test_file.tmp'}

    # When
    hmm_generator.validate(arguments)
