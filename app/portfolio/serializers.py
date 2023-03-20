from rest_framework import serializers

from portfolio import models


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Character
        fields = ['name', 'slug', 'sex', 'alive', 'first_appearance']
        extra_kwargs = {
            'slug': {'required': False}
        }
