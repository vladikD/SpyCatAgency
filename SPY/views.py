from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Mission, Target, SpyCat
from .serializers import MissionSerializer, SpyCatSerializer


class SpyCatViewSet(viewsets.ModelViewSet):
    queryset = SpyCat.objects.all()
    serializer_class = SpyCatSerializer


class MissionViewSet(viewsets.ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        mission = self.get_object()
        if mission.cat and not mission.is_complete:
            return Response(
                {"detail": "Cannot delete a mission that is assigned to a cat."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        mission.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        mission = self.get_object()
        if mission.is_complete:
            return Response(
                {"detail": "Cannot update a completed mission."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if 'targets' in request.data:
            targets_data = request.data.pop('targets')

            for target_data in targets_data:
                target_id = target_data.get('id')
                if not target_id:
                    return Response({"detail": "Each target must include an 'id'."}, status=status.HTTP_400_BAD_REQUEST)
                try:
                    target = mission.targets.get(id=target_id)
                except Target.DoesNotExist:
                    return Response({"detail": f"Target with id {target_id} does not exist."}, status=status.HTTP_404_NOT_FOUND)
                target.notes = target_data.get('notes', target.notes)
                target.complete = target_data.get('complete', target.is_complete)
                target.save()

        serializer = self.get_serializer(mission, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def assign_cat(self, request, pk=None):
        mission = self.get_object()
        cat_id = request.data.get('cat_id')

        try:
            cat = SpyCat.objects.get(id=cat_id)
        except SpyCat.DoesNotExist:
            return Response(
                {"detail": "Cat with the provided id does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )

        if Mission.objects.filter(cat=cat, is_complete=False).exists():
            return Response(
                {"detail": "This cat is already assigned to an active mission."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        mission.cat = cat
        mission.save()

        return Response(
            {"detail": f"Cat {cat.name} successfully assigned to mission."},
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=['get'])
    def list_missions(self, request):
        missions = Mission.objects.all()
        serializer = MissionSerializer(missions, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def get_single_mission(self, request, pk=None):
        mission = self.get_object()
        serializer = MissionSerializer(mission)
        return Response(serializer.data)
