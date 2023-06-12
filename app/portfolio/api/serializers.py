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


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Artist
        fields = '__all__'
        extra_kwargs = {
            'slug': {'required': False}
        }


class ArtistImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to artists."""

    class Meta:
        model = models.Artist
        fields = ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {
            'image': {'required': True}
        }


class ArtSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Art
        fields = '__all__'
        extra_kwargs = {
            'tags': {'required': False},
            'characters': {'required': False},
        }


class ArtImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to art."""

    class Meta:
        model = models.Art
        fields = ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {
            'image': {'required': True}
        }
