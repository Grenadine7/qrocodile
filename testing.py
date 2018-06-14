#!/usr/bin/env python3

import os,json,requests

default_hostname = '192.168.188.12'
base_url = 'http://' + default_hostname + ':5005'
response = requests.get(base_url + '/zones')


def isolate_device_playing(device):
    response = requests.get(base_url + '/zones')
    for i, val in enumerate(response.json()):
        member_list = [] # create a list of members per coordinator
        for i3,n in enumerate(response.json()[i]['members']):
            member_list.append(str(response.json()[i]['members'][i3]['roomName']))
        for i3, val3 in enumerate(member_list):
            if member_list[i3].lower() != device.lower():
                print('removed member ' + val3 + ' from ' + device)
                requests.get(base_url + '/' + val3 + '/leave/' + device) # device will be the one left active
    print(device + ' is now the single current device')

def find_device_playing(device):
    #global all_rooms
    response = requests.get(base_url + '/zones')
    all_rooms = {}  # blank dict
    all_members = {}
    for i, val in enumerate(response.json()):
        coordinator_index = str(i)
        members_qty = str(val['members'].__len__())
        coord_state = response.json()[i]['coordinator']['state']['playbackState']
        coord_name = response.json()[i]['coordinator']['roomName']
        #all_rooms.update[{'coordinator': coord_name}]
        all_rooms.update({'coordinator' : coord_name })
        print('coordinator ' + coordinator_index + ' named ' + coord_name + ' with state ' + coord_state + ' has ' + members_qty + ' members.')
        for i2, val2 in enumerate(val['members']):
            member_index = str(i2)
            member_state = str(val2['state']['playbackState'])
            member_name = str(val2['roomName'])
            #all_rooms[{'coordinator': coord_name}].update({'member': member_name})
            print(type(all_rooms))
            all_members.update({'member' : member_name})
            #all_rooms['coordinator'].update({'member': member_name})
            if int(members_qty) > 1:
                if member_name == device:
                    print('I found the device, it\'s: ' + coordinator_index + ' coordinator ' + coord_name + ' member ' + member_index)
                    #print('removing ' + member_name + ' from ' + device)
                else:
                    print('I did not find the device')
                    #all_rooms.append(member_name)
                print('member ' + member_index + ' called ' + member_name + ' with state ' + member_state + '\n')
        all_rooms['coordinator'].update(all_members)
        print(all_rooms)



def list_device_playing():
    response = requests.get(base_url + '/zones')
    for i, val in enumerate(response.json()):
        all_rooms = []  # blank list
        coordinator_index = str(i)
        members_qty = str(val['members'].__len__())
        coord_state = response.json()[i]['coordinator']['state']['playbackState']
        coord_name = response.json()[i]['coordinator']['roomName']
        print('coordinator ' + coordinator_index + ' named ' + coord_name + ' with state ' + coord_state + ' has ' + members_qty + ' members.')
        for i2, val2 in enumerate(val['members']):
            member_index = str(i2)
            member_state = str(val2['state']['playbackState'])
            member_name = str(val2['roomName'])
            print('member ' + member_index + ' called ' + member_name + ' with state ' + member_state + '\n')
        #print(all_rooms)

#find_device_playing('kitchen')
list_device_playing()