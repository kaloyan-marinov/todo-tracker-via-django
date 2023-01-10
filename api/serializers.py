from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            "title",
            "completed",
        )
        # The previous statement can be replaced with:
        # fmt: off
        '''
        fields = "__all__"
        '''
        # fmt: on
