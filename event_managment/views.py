from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


from .serializer import VenueSerializer , EventSerializer
from .models import Venue , Event

import requests

from Event.settings import EVENTBRITE_TOKEN

import json


class VenueView(viewsets.ModelViewSet):
    
    serializer_class = VenueSerializer
    queryset = Venue.objects.all()
    http_method_names = ['get','post']
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = self.queryset
        return qs.select_related('User_id').filter(User_id = self.request.user)

    def create(self,request):
        '''Create the venue with the reference of the organization 
            and the store the data into db after successful save into the eventbrite'''
        try:
            response = requests.post(f'https://www.eventbriteapi.com/v3/organizations/{request.user.organization_id}/venues/', data=json.dumps(request.data) ,headers={"Content-Type":"application/json" , "Authorization": f"Bearer {EVENTBRITE_TOKEN}"})
            if response.status_code == 200:
                res = response.json()

                data = {}
                data['Venue_id'] = res['id']
                data['User_id'] = request.user.id
                data['address'] = res['address']['address_1']

                serializer = self.serializer_class(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()

                return Response({"response":serializer.data}, status=status.HTTP_200_OK)

            else:
                return Response({"response":response.json()}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"Message":"Intenal server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class EventView(viewsets.ModelViewSet):
    
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    http_method_names = ['get','post']
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        '''Validate and check the record against the login user'''
        qs = self.queryset
        return qs.select_related('Venue_id').select_related('Venue_id__User_id').filter(Venue_id__User_id = self.request.user)

    def retrieve(self,request,pk=None):
        '''Validate and check the record against the login user'''
        try:
            qs = self.get_queryset().filter(id=pk)
            if qs:

                '''All the required information is getting from the eventbrite api to repersent to the user end'''

                qs = qs[0]
                response = requests.get(f'https://www.eventbriteapi.com/v3/events/{qs.Event_id}/', headers={"Content-Type":"application/json" , "Authorization": f"Bearer {EVENTBRITE_TOKEN}"})

                if response.status_code == 200: 
                    res = {'event':response.json()}
                    response = requests.get(f'https://www.eventbriteapi.com/v3/events/{qs.Event_id}/ticket_classes/{qs.ticket_id}/', headers={"Content-Type":"application/json" , "Authorization": f"Bearer {EVENTBRITE_TOKEN}"})

                    if response.status_code == 200: 
                        res['ticket'] = response.json()
                        return Response({"response":res}, status=status.HTTP_200_OK)        
                    else:
                        return Response({"response":response.json()}, status=status.HTTP_400_BAD_REQUEST)

                else:
                    return Response({"response":response.json()}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"response":"User is not authorize to access this content"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"Message":"Intenal server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def create(self,request):
        '''Create the event with ticket price and details into database and in eventbrite server'''
        try:
            response = requests.post(f'https://www.eventbriteapi.com/v3/organizations/{request.user.organization_id}/events/', data=json.dumps({'event':request.data['event']}) ,headers={"Content-Type":"application/json" , "Authorization": f"Bearer {EVENTBRITE_TOKEN}"})
            if response.status_code == 200:
                res = response.json()
            
                data = {}
                data['Venue_id'] = Venue.objects.get(Venue_id=res['venue_id']).id
                data['User_id'] = request.user.id
                data['Event_id'] = res['id']
                data['name'] = res['name']['text']
                data['description'] = res['description']['text']
                data['start_time'] = res['start']['local']
                data['end_time'] = res['end']['local']

                event = res['id']
                response = requests.post(f'https://www.eventbriteapi.com/v3/events/{event}/ticket_classes/', data=json.dumps({'ticket_class':request.data['ticket_class']}) ,headers={"Content-Type":"application/json" , "Authorization": f"Bearer {EVENTBRITE_TOKEN}"})

                if response.status_code == 200:
                    res = response.json()

                    data['ticket_id'] = res['id']

                    serializer = self.serializer_class(data=data)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()

                    return Response({"response":serializer.data}, status=status.HTTP_200_OK)

                else:
                    return Response({"response":response.json()}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"response":response.json()}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"Message":"Intenal server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        