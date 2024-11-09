import requests
from rest_framework import serializers
from .models import SpyCat, Mission, Target

class SpyCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpyCat
        fields = '__all__'

    def validate_breed(self, value):
        try:
            url = 'https://api.thecatapi.com/v1/breeds'
            response = requests.get(url)
            response.raise_for_status()

            breeds = [breed['name'] for breed in response.json()]
            if value not in breeds:
                raise serializers.ValidationError("Invalid breed. Please provide a recognized breed.")
        except requests.RequestException:
            raise serializers.ValidationError("Unable to verify breed at this time due to network issues.")
        return value


class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ['id', 'name', 'country', 'notes', 'is_complete']
        read_only_fields = ['id', 'is_complete']


class MissionSerializer(serializers.ModelSerializer):
    targets = TargetSerializer(many=True)
    is_complete = serializers.BooleanField(required=False)

    class Meta:
        model = Mission
        fields = ['id', 'cat', 'targets', 'is_complete']
        read_only_fields = ['cat']

    def create(self, validated_data):
        targets_data = validated_data.pop('targets')
        mission = Mission.objects.create(**validated_data)
        for target_data in targets_data:
            Target.objects.create(mission=mission, **target_data)
        return mission

    def update(self, instance, validated_data):
        targets_data = validated_data.pop('targets', None)

        instance.is_complete = validated_data.get('is_complete', instance.is_complete)
        instance.save()

        if targets_data:
            for target_data in targets_data:
                if 'id' in target_data:
                    try:
                        target = instance.targets.get(id=target_data['id'])
                        target.notes = target_data.get('notes', target.notes)
                        target.is_complete = target_data.get('is_complete', target.is_complete)  # Оновлення 'is_complete'
                        target.save()
                    except Target.DoesNotExist:
                        raise serializers.ValidationError(f"Target with id {target_data['id']} does not exist.")
                else:
                    raise serializers.ValidationError("Each target must include an 'id' field to update.")

        return instance


class MissionUpdateTargetsSerializer(serializers.ModelSerializer):
    targets = TargetSerializer(many=True)

    class Meta:
        model = Mission
        fields = ['targets']

    def update(self, instance, validated_data):
        targets_data = validated_data.pop('targets', [])

        for target_data in targets_data:
            target_id = target_data.get('id')

            if not target_id:
                raise serializers.ValidationError("Each target must include an 'id'.")

            try:
                target = instance.targets.get(id=target_id)
                target.notes = target_data.get('notes', target.notes)
                target.is_complete = target_data.get('is_complete', target.is_complete)
                target.save()
            except Target.DoesNotExist:
                raise serializers.ValidationError(f"Target with id {target_id} does not exist.")

        return instance
