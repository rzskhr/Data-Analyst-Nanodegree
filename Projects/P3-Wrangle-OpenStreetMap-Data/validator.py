import cerberus     # http://docs.python-cerberus.org/en/stable/
import schema


SCHEMA = schema.schema


def validate_element(element, validator, schema=SCHEMA):
    """
    Raise ValidationError if element does not match schema
    """
    if validator.validate(element, schema) is not True:
        # field, errors = next(validator.errors.items())
        # ref: https://stackoverflow.com/questions/4002874/non-destructive-version-of-pop-for-a-dictionary
        field, errors = next(iter(validator.errors.items()))
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_strings = (
            "{0}: {1}".format(k, v if isinstance(v, str) else ", ".join(v))
            for k, v in errors.items()
        )
        raise cerberus.ValidationError(
            message_string.format(field, "\n".join(error_strings))
        )
