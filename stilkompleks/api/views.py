from django.db.models import query
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.decorators import api_view
from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse

# Create your views here.


class ObektiView(generics.ListAPIView):
    queryset = Obekti.objects.all()
    serializer_class = ObektiSerializer


class CreateObektView(APIView):
    serializer_class = CreateObektiSerializer

    def post(self, request, format=None):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            print(serializer.data)
            name = serializer.data.get('name')
            investor = serializer.data.get('investor')
            address = serializer.data.get('address')
            
            obekt = Obekti(name=name, investor=investor,
                        address=address)
            obekt.save()

            return Response(CreateObektiSerializer(obekt).data, status=status.HTTP_201_CREATED)

        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)

class UpdateObektView(APIView):
    serializer_class = UpdateObektiSerializer

    def patch(self, request, format=None):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            print(serializer.data)
            id = serializer.data.get('id')
            print(id)
            obekt = Obekti.objects.filter(id=id)
            if obekt.exists():
                print()
                obekt = obekt[0]
                obekt.name = serializer.data.get('name')
                obekt.investor = serializer.data.get('investor')
                obekt.address = serializer.data.get('address')
                materials = serializer.data.get('material')
                mats = []
                if len(materials):
                    for m in materials:
                        obekt.material.add(m)


                obekt.save(update_fields=['name', 'address', 'investor'])

                return Response(CreateObektiSerializer(obekt).data, status=status.HTTP_200_OK)

            return Response({'Bad Request': 'Obekt not found...'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)


class DeleteObektView(APIView):

    def delete(self, request, pk, format=None):
        
        try:
            obekt = Obekti.objects.get(id=pk)
        except Obekti.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        obekt.delete()
        return Response({'Success': 'Obekt deleted'}, status=status.HTTP_204_NO_CONTENT)



class PersonalView(generics.ListAPIView):
    queryset = Personal.objects.all()
    serializer_class = PersonalSerializer

class CreatePersonalView(APIView):
    serializer_class = CreatePersonalSerializer

    def post(self, request, format=None):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            name = serializer.data.get('name')
            position = serializer.data.get('position')
            obekt = serializer.data.get('obekt')
            mail = serializer.data.get('mail')
            phone_number = serializer.data.get('phone_number')
            machine = serializer.data.get('machine')

            try:
                obekt = Obekti.objects.get(pk=int(obekt))
            except:
                obekt = ''
            try:
                machine = Machine.objects.get(pk=int(machine))
            except:
                machine = ''

            if position=='Tc':
                if len(Obekti.objects.filter(personal__position='Tc', id=obekt.id)):
                    return Response({'Bad Request': 'This obekt already has assigned technicheski...'}, status=status.HTTP_400_BAD_REQUEST)
            person = Personal(name=name, position=position, obekt=obekt, mail=mail, phone_number=phone_number, machine=machine)
            person.save()

            return Response(CreatePersonalSerializer(person).data, status=status.HTTP_201_CREATED)

        return Response({'Bad Request': 'This obekt already has technicheski...'}, status=status.HTTP_400_BAD_REQUEST)

class UpdatePersonalView(APIView):
    serializer_class = UpdatePersonalSerializer

    def patch(self, request, format=None):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            id = serializer.data.get('id')
            print(id)
            person = Personal.objects.filter(id=id)
            if person.exists():
                person = person[0]
                person.name = serializer.data.get('name')
                position = serializer.data.get('position')
                obekt = serializer.data.get('obekt')
                person.mail = serializer.data.get('mail')
                person.phone_number = serializer.data.get('phone_number')
                
                try:
                    obekt = Obekti.objects.get(pk=int(obekt))
                except:
                    obekt = ''

                #check if we are updating the person as Technical to new obekt and that obekt already has another technical  
                if position =='Tc' and person.position != 'Tc':
                    if len(Obekti.objects.filter(personal__position='Tc', id=obekt.id)):
                        return Response({'Bad Request': 'This obekt already has assigned technicheski...'}, status=status.HTTP_400_BAD_REQUEST)
                person.position = position
                person.obekt = obekt
                
                person.save(update_fields=['name', 'position', 'obekt', 'mail', 'phone_number'])

                return Response(CreatePersonalSerializer(person).data, status=status.HTTP_200_OK)
            return Response({'Bad Request': 'Person not found...'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'Bad Request': 'Serializer invalid...'}, status=status.HTTP_400_BAD_REQUEST)
      
class DeletePersonalView(APIView):

    def delete(self, request, pk, format=None):
        
        try:
            personal = Personal.objects.get(id=pk)
        except Personal.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        personal.delete()
        return Response({'Success': 'Personal deleted'}, status=status.HTTP_204_NO_CONTENT)
'''

@api_view(['DELETE'])
def delete_obekt(request, pk):
    """
    delete obekt.
    """
    try:
        snippet = Obekti.objects.get(pk=pk)
    except Obekti.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    snippet.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


class GetRoom(APIView):
    serializer_class = RoomSerializer
    lookup_url_kwarg = 'code'

    def get(self, request, format=None):
        code = request.GET.get(self.lookup_url_kwarg)

        if code != None:
            room = Room.objects.filter(code=code)
            if len(room) > 0:
                data = RoomSerializer(room[0]).data
                data['is_host'] = self.request.session.session_key == room[0].host
                return Response(data, status=status.HTTP_200_OK)
            return Response({'Room Not Found': 'Invalid Room Code.'}, status=status.HTTP_400_BAD_REQUEST) 
        return Response({'Bad Request': 'Code Not Found.'}, status=status.HTTP_400_BAD_REQUEST) 


class JoinRoom(APIView):
    serializer_class = RoomSerializer
    lookup_url_kwarg = 'code'
    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        code = request.data.get(self.lookup_url_kwarg);
        if code != None:
            room_result = Room.objects.filter(code=code)
            if len(room_result) > 0:
                self.request.session['room_code'] = code
                return Response({'message': 'Room Joined!'}, status=status.HTTP_200_OK)

            return Response({'Bad request': 'Invalid Room Code!'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'Bad request': 'Invalid post data, code not found!'}, status=status.HTTP_400_BAD_REQUEST)


class CreateRoomView(APIView):
    serializer_class = CreateRoomSerializer

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get('guest_can_pause')
            votes_to_skip = serializer.data.get('votes_to_skip')
            host = self.request.session.session_key
            queryset = Room.objects.filter(host=host)
            if queryset.exists():
                room = queryset[0]
                room.guest_can_pause = guest_can_pause
                room.votes_to_skip = votes_to_skip
                room.save(update_fields=['guest_can_pause', 'votes_to_skip'])
                self.request.session['room_code'] = room.code
                return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)
            else:
                room = Room(host=host, guest_can_pause=guest_can_pause,
                            votes_to_skip=votes_to_skip)
                room.save()
                self.request.session['room_code'] = room.code
                return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)

        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)

class CheckUserInRoom(APIView):
    def get(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        data = {
            'code': self.request.session.get("room_code")
        }

        return JsonResponse(data, status=status.HTTP_200_OK)

class LeaveRoom(APIView):
    def post(self, request, format=None):
        if 'room_code' in self.request.session:
            self.request.session.pop('room_code')

            host_id = self.request.session.session_key
            room = Room.objects.filter(host=host_id)
            if len(room) > 0:
                room = room[0]
                room.delete()
        return Response({'message': 'Success!'}, status=status.HTTP_200_OK)

class UpdateRoom(APIView):
    serializer_class = UpdateRoomSerializer

    

    def patch(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get('guest_can_pause')
            votes_to_skip = serializer.data.get('votes_to_skip')
            code = serializer.data.get('code')

            queryset = Room.objects.filter(code=code)
            if not queryset.exists():
                return Response({'msg': 'Room not found'}, status=status.HTTP_404_NOT_FOUND)

            room = queryset[0]
            user_id = self.request.session.session_key
            if room.host != user_id:
                return Response({'msg': 'You are not host of this room'}, status=status.HTTP_403_FORBIDDEN)

            room.guest_can_pause = guest_can_pause
            room.votes_to_skip = votes_to_skip
            room.save(update_fields=['guest_can_pause','votes_to_skip'])

            return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)

        return Response({'Bad Request': 'Invalid data!'}, status=status.HTTP_400_BAD_REQUEST)


class UserInfo(APIView):
    def get(self, request, format=None):
        if request.user.is_authenticated:
            user = self.request.user.username
        
            return Response({'user' : str(user)}, status=status.HTTP_200_OK)
        else:
            return Response({'Error' : "Not Auth"}, status=status.HTTP_401_UNAUTHORIZED)
        #return JsonResponse(data, status=status.HTTP_200_OK)
'''