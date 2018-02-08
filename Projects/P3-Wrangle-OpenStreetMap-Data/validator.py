import cerberus     # http://docs.python-cerberus.org/en/stable/
import schema
import pprint

SCHEMA = schema.schema


def validate_element(element, validator, schema=SCHEMA):
    """
    Raise ValidationError if element does not match schema
    """
    if validator.validate(element, schema) is not True:
        # field, errors = next(validator.errors.items())

        field, errors = next(iter(validator.errors.items()))
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"

        # testing this line
        error_strings = pprint.pformat(errors)

        # error_strings = (
        #     "{0}: {1}".format(k, v if isinstance(v, str) else ", ".join(v))
        #     for k, v in errors.items()
        # )

        # raise Exception(message_string.format(field, error_strings))

        # test test test
        print("\nTHERE IS AN ERROR MESSAGE\n")
        print(message_string.format(field, error_strings))
        print("\nElement which has error:\n", element)
        print("----------------------------------------------------\n")

        # raise cerberus.ValidationError(
        #     message_string.format(field, "\n".join(error_strings))
        # )
