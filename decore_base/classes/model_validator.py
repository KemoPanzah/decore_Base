from cerberus import Validator

class Model_validator(Validator):
    def __init__(self, p_model, *args, **kwargs):
        self.model = p_model
        Validator.__init__(self, *args, **kwargs)

    def _validate_unique(self, unique, field, value):
        # TODO keine Ahnung was das hier soll, bitte nochmal genau nachlesen aber ohne den DocString gibt es eine Warung
        "{'type': 'boolean'}"
        if unique:
            t_item = self.model.get_or_none(getattr(self.model, field) == value)
            if t_item is not None and t_item.id != self.document.get('id'):
                self._error(field, "Value already exists")