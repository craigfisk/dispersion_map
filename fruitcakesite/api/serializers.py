from django.core import serializers

class QuerySetSerializer(serializers.get_serializer('json')):
    pass


class SingleObjectSerializer(QuerySetSerializer):
    def serialize(self, obj, **options):
        # Wrap the object in a list in order to use the standard serializer
        return super(SingleObjectSerializer, self).serialize([obj], **options)

    def getvalue(self):
        # Strip off the outer list for just a single item
        value = super(SingleObjectSerializer, self).getvalue()
        return value.strip('[]\n')
