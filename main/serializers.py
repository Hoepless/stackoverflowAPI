from rest_framework import serializers

from .models import Problem, Image, Reply, Comment


class TypeBaseSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        abstract = True


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ('image', )


class ProblemSerializer(TypeBaseSerializer):
    # author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Problem
        fields = ('id', 'title', 'description', 'author')

    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user
        problem = Problem.objects.create(author=author, **validated_data)
        image_list = request.FILES
        for image in image_list.getlist('images'):
            Image.objects.create(problem=problem, image=image)
        return problem

    def update(self, instance, validated_data):
        request = self.context.get('request')
        for key, value in validated_data.items():
            setattr(instance, key, value)
        image_list = request.FILES
        instance.images.all().delete()
        for image in image_list.getlist('images'):
            Image.objects.create(problem=instance, image=image)
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['images'] = ImageSerializer(instance.images.all(), many=True, context=self.context).data
        action = self.context.get('action')
        #!  print(instance.replies.all())
        if action == 'retrieve':
            representation['replies'] = ReplySerializer(instance.replies.all(), many=True).data
        elif action == 'list':
            representation['replies'] = instance.replies.count()
        return representation


class ReplySerializer(TypeBaseSerializer):
    # author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Reply
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user
        reply = Reply.objects.create(author=author, **validated_data)
        return reply

    def to_representation(self, instance):
        representation = super().to_representation(instance)


class CommentSerializer(TypeBaseSerializer):
    # author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user
        comment = Comment.objects.create(author=author, **validated_data)
        return comment
