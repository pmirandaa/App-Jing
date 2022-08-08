from rest_framework import serializers

# Adapted from
# https://www.django-rest-framework.org/api-guide/serializers/#dynamically-modifying-fields
# https://stackoverflow.com/a/57046233/
# https://stackoverflow.com/a/41063577/
class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)
        excluded_fields = kwargs.pop("excluded_fields", None)
        extra_fields = kwargs.pop("extra_fields", None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
        
        if excluded_fields is not None:
            # Drop any fields that are specified in the `excluded_fields` argument.
            for field_name in excluded_fields:
                self.fields.pop(field_name)

    # Add fields specified in the `extra_fields` argument.
    # They must be declared with their corresponding serializer.
    def get_field_names(self, declared_fields, info):
        expanded_fields = super(DynamicFieldsModelSerializer, self).get_field_names(declared_fields, info)
        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + list(self.Meta.extra_fields)
        else:
            return expanded_fields