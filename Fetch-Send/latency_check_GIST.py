#!/usr/bin/env python
##################Check latency source: GIST-NUC/103.22.221.62#############################
#######edited by ahmad, email: ahmad@smartx.kr#############

"""
esmond-ps-get - client to fetch perfsonar test results.
"""

# for the script name:
# pylint: disable=invalid-name

import csv
import string
from kafka import KafkaProducer
from kafka.errors import KafkaError
import time
from esmond_client.perfsonar.query import ApiConnect, ApiFilters
#import  esmond.api.client.perfsonar.post
from esmond_client.perfsonar.util import (
    data_format_factory,
    output_factory,
    perfsonar_client_filters,
    perfsonar_client_opts,
)


def main():
    """main loop/execute query."""
    filters = ApiFilters()

    filters.verbose = True

    filters.time_start = time.time() - 1800
    filters.time_end =  time.time()

    ip_address='103.22.221.62'


################################################## Add event type, tool name  ##################################
    filters.tool_name = 'pscheduler/ping'#  filters.tool_name = 'pscheduler/iperf3'

    filters.event_type='histogram-rtt'           #filters.event_type='throughput'
    filters.source = ip_address
    conn = ApiConnect('http://'+ip_address, filters)

###    print  'Source,  destination,    tool_name,      ip_packet_interval,     event_type'

    for md in conn.get_metadata():
      print md.source,md.destination,md.tool_name,md.ip_packet_interval,md.get_event_type


    print("------------------------------------------------------------------------------")
    print("------------------------------------------------------------------------------")
    print("------------------------------------------------------------------------------")
#uncomment###    for md in conn.get_metadata():
#uncomment##      print md

    for md in conn.get_metadata():
     for et in md.get_all_event_types():
#        et= md.get_event_type('throughput')
        dpay = et.get_data()
        print et.event_type                                     #get the event type

################################################## Filter  event type##################################
#        if et.event_type=='histogram-rtt' or  et.event_type=='histogram-ttl':
        if et.event_type=='histogram-rtt':
         for dp in dpay.data:
#          print (md.source,md.destination,dp.ts, dp.val, md.tool_name, et.event_type).replace("u\"","\"").replace("u\'","\'")
#line 57
          i=0
          source= md.source
          destination=md.destination
          time_stamp=dp.ts
          for key,value in dp.val.items():
           if i==1:
            value1=key
           else:
            i+=1
            value1=key


          value=dp.val
          tool_name=md.tool_name
          event_type= et.event_type
#          print source,destination,time_stamp,value,tool_name,event_type

#          MESSAGE= str(source)+','+ str(destination)+','+ str(time_stamp)+','+ str(value)+','+str(tool_name)+','+ str(event_type)
          MESSAGE1= str(source)+','+ str(destination)+','+ str(time_stamp)+','+ str(value1)+','+str(tool_name)+','+ str(event_type)
#          print MESSAGE
          print MESSAGE1
          print "Kafka"

################################################## Send data through KAFKA to Visibility Center  ##################################

          producer = KafkaProducer(bootstrap_servers=['vc.manage.overcloud:9092'])
          producer.send('active_monitoring_latency', key=b'latency', value=MESSAGE1)
          with open('measurement_data.csv', 'a') as newFile:
             newFileWriter = csv.writer(newFile, delimiter=' ',escapechar=' ', quoting=csv.QUOTE_NONE)
             newFileWriter.writerow([MESSAGE1])

#          with open('latency_test.txt', 'a') as file:
#            file.write(MESSAGE1+" ")


#    file.close()
    print("/////////////////////////////////////Change Destination as base machine///////////////////////////////////////////////////////")


    print ("Destination = '103.22.221.62'")
    filters.destination = '103.22.221.62'
    ip_addresses=("203.191.48.228","203.80.21.4","161.200.25.99")
    for i in range(len(ip_addresses)):
     filters.source=ip_addresses[i]
     conn = ApiConnect('http://'+ip_address, filters)
     for md in conn.get_metadata():
      for et in md.get_all_event_types():
       dpay = et.get_data()
       print et.event_type, md.source,md.destination, md.tool_name, md.measurement_agent                                        #get the event type
################################################## Filter  event type##################################
       if et.event_type=='histogram-rtt':
 #      if et.event_type=='throughput':
        for dp in dpay.data:
         print md.source,md.destination,dp.ts, dp.val,md.tool_name, et.event_type



############################################Wroking code##############################
#        print et.event_type
#        et= md.get_event_type('throughput') #error
#        print(et)
############################################Wroking code##############################

#        dpay=et.get_data()#error
#       print(dpay) #error

##     print dpay.data_type
##     for dp in dpay.data:
##       print dp.ts, dp.val

#      for et in md.get_all_event_types():
#       print et.event_type
#     print md.get_event_type('throughput')
#     print md.destination
#      print md.throughput
#    print output.get_output()

if __name__ == '__main__':
    main()
