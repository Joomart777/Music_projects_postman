from rest_framework import serializers

from music_app.models import Music, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = '__all__'

        # fields = ('title')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        print(representation)

        category = CategorySerializer(Category.objects.get(music=instance.id)).data
        print(category)
        representation['category'] = category

        return representation