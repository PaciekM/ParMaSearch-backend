from rest_framework import serializers


class StringListField(serializers.ListField):
    child = serializers.ListField()


class DocumentSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    text = serializers.CharField(max_length=2000)
    # subject = serializers.CharField(max_length=50)
    title_vector = serializers.CharField(
        max_length=500)
    # text_vector = serializers.CharField(
    #     max_length=500)
