from rest_framework import serializers

from portfolio import models


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Character
        fields = ['name', 'slug', 'sex', 'alive',
                  'first_appearance', 'created_by']
        extra_kwargs = {
            'slug': {'required': False}
        }


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = '__all__'
