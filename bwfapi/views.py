from datetime import datetime

import pytz
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly

from .models import Group, Event, UserProfile, Member, Comment, Bet
from .serializers import GroupSerializer, EventSerializer, GroupFullSerializer, UserSerializer, UserProfileSerializer, \
    ChangePasswordSerializer, MemberSerializer, CommentSerializer, EventFullSerializer, BetSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    @action(methods=['PUT'], detail=True, serializer_class=ChangePasswordSerializer,
            permission_classes=[IsAuthenticated])
    def change_password(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            if not user.check_password(serializer.data.get('old_password')):
                return Response({'message': 'Wrong old password'}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.data.get('new_password'))
            user.save()
            return Response({'message': 'Password Updated'}, status=status.HTTP_200_OK)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = GroupFullSerializer(instance, many=False, context={'request': request})
        return Response(serializer.data)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = EventFullSerializer(instance, many=False, context={'request': request})
        return Response(serializer.data)


class BetViewSet(viewsets.ModelViewSet):
    queryset = Bet.objects.all()
    serializer_class = BetSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        response = {'message': "Method not allowed"}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        response = {'message': "Method not allowed"}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def check_user_in_group(self, event, user):
        try:
            return Member.objects.filter(user=user, group=event.group).exists()
        except ObjectDoesNotExist:
            return False

    @action(detail=False, methods=['POST'], url_path='place_bet')
    def place_bet(self, request):
        if 'event' in request.data and 'score1' in request.data and 'score2' in request.data:
            event_id = request.data['event']
            event = Event.objects.get(id=event_id)

            in_group = self.check_user_in_group(event, request.user)

            # if event.time > datetime.now(pytz.UTC) and in_group:
            if in_group:
                score_1 = request.data['score1']
                score_2 = request.data['score2']

                try:
                    # Updating bet
                    my_bet = Bet.objects.get(event=event_id, user=request.user.id)
                    my_bet.score_1 = score_1
                    my_bet.score_2 = score_2
                    my_bet.save()
                    serializer = BetSerializer(my_bet, many=False)
                    response = {'message': "Bet Updated", 'new': False, 'result': serializer.data}
                    return Response(response, status=status.HTTP_200_OK)

                except ObjectDoesNotExist:
                    # Creating a new bet
                    my_bet = Bet.objects.create(event=event, user=request.user, score_1=score_1, score_2=score_2)
                    serializer = BetSerializer(my_bet, many=False)
                    response = {'message': "Bet Created", 'new': True, 'result': serializer.data}
                    return Response(response, status=status.HTTP_200_OK)

            else:
                response = {'message': "The event has ended. No more bets allowed."}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

        else:
            response = {'message': "Wrong params."}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(methods=['POST'], detail=False)
    def join(self, request):
        if 'group' in request.data and 'user' in request.data:
            try:
                group = Group.objects.get(id=request.data['group'])
                user = User.objects.get(id=request.data['user'])
                member = Member.objects.create(group=group, user=user, admin=False)
                serializer = MemberSerializer(member, many=False)
                response = {'message': "Joined to  a group", 'results': serializer.data}
                response_status = status.HTTP_200_OK
            except (Exception,):
                response = {'message': 'Can not join to the group'}
                response_status = status.HTTP_400_BAD_REQUEST
        else:
            response = {'message': 'Wrong params'}
            response_status = status.HTTP_400_BAD_REQUEST

        return Response(response, status=response_status)

    @action(methods=['post'], detail=False)
    def leave(self, request):
        if 'group' in request.data and 'user' in request.data:
            try:
                group = Group.objects.get(id=request.data['group'])
                user = User.objects.get(id=request.data['user'])
                member = Member.objects.get(group=group, user=user)
                member.delete()
                response = {'message': "Left the group"}
                response_status = status.HTTP_200_OK
            except (Exception,):
                response = {'message': 'Can not leave the group'}
                response_status = status.HTTP_400_BAD_REQUEST
        else:
            response = {'message': 'Wrong params'}
            response_status = status.HTTP_400_BAD_REQUEST

        return Response(response, status=response_status)


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)  # TODO: arguments of super
        token = Token.objects.get(key=response.data['token'])
        user = User.objects.get(id=token.user_id)
        user_serializer = UserSerializer(user)
        return Response({'token': token.key, 'user': user_serializer.data})
