#----------------------------------------------------------------------------------------------------#
# basic IoT-Chat app on Pubnub with latest Python SDK                                                #
# import function from standard librairy section: PubNub                                             #
#----------------------------------------------------------------------------------------------------#
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from threading import Thread

#----------------------------------------------------------------------------------------------------#
# initialize the client                                                                              #
#----------------------------------------------------------------------------------------------------#
# create pubnub configuration object
pnconfig = PNConfiguration()

# set pubnub publish and subscribe keys
pnconfig.subscribe_key = 'demo'
pnconfig.publish_key = 'demo'
# assugn pubnub channel name
my_channel = 'awesomeChannel'

pnconfig.ssl = False

# let assign each user a basic user id for the basic chat app
pnconfig.uuid = 'Yann'

# create pubnub object with pubnub configuration object
pubnub = PubNub(pnconfig)

#----------------------------------------------------------------------------------------------------#
# adding listenner and publisher and function                                                        #
#----------------------------------------------------------------------------------------------------#
def my_publish_callback(envelope, status):
    # Check whether request successfully completed or not
    if not status.is_error():
        pass  # Message successfully published to specified channel.
    else:
        pass  # Handle message publish error. Check 'category' property to find out possible issue
        # because of which request did fail.
        # Request can be resent using: [status retry];

# create listner object to read the msg from the Broker/Server
class MySubscribeCallback(SubscribeCallback):
    def presence(self, pubnub, presence):
        pass  # handle incoming presence data

    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            pass  # This event happens when radio / connectivity is lost

        elif status.category == PNStatusCategory.PNConnectedCategory:
            # Connect event. You can do stuff like publish, and know you'll get it.
            # Or just use the connected event to confirm you are subscribed for
            # UI / internal notifications, etc
            pubnub.publish().channel(my_channel).message(
                "hello World! I'm " + pnconfig.uuid + "!!").async(my_publish_callback)
        elif status.category == PNStatusCategory.PNReconnectedCategory:
            pass
            # Happens as part of our regular operation. This event happens when
            # radio / connectivity is lost, then regained.
        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            pass
            # Handle message decryption error. Probably client configured to
            # encrypt messages and on live data feed it received plain text.

    def message(self, pubnub, message):
        msg = message.message
        if type(msg) == dict:
            if msg.get('from') != pubnub.uuid:   
                print(msg)
                pass  # Handle new message stored in message.message
        else:
            print(msg)

# let create a function to send the message
def sendMessage():
    message = input("Enter:")
    # publish the data to the mentioned channel
    # message({"from": pubnub.uuid, "Message": message})
    pubnub.publish().channel(my_channel).message(
        {"from": pubnub.uuid, "Message": message}).async(my_publish_callback)

# let call sendMessage function from the thread
T = Thread(target=sendMessage)
T.start()

#----------------------------------------------------------------------------------------------------#
# add listner object to pubnub object to subscribe it
my_listener = MySubscribeCallback()
pubnub.add_listener(my_listener)
# subscribe the channel (Runs in background)
while True:
    pubnub.subscribe().channels(my_channel).execute()

# wait for the listner object to connect to the Broker.Channel
# MySubscribeCallback().wait_for_connect()
# print confirmation msg
# print('connected')

# publish the data to the mentioned channel
# pubnub.publish().channel(channel).message(data).sync()

# while True:                                                      # Infinite loop
#    result = MySubscribeCallback.wait_for_message_on(my_channel) # Read the new msg on the channel
#    print(result.message)                                        # print the new msg

#----------------------------------------------------------------------------------------------------#
