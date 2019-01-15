from flask import Flask, render_template, request, redirect
import os
import Queue
import socket
# from flaskext.mysql import MySQL

app = Flask(__name__)

class pub :
    def __init__ (self, name, topic) :
        self.name = name
        self.topic = []
        self.mess =[]
        self.topic.append(topic)
        print("publisher", self.name," is constructed")
    
    def __del__ (self):
        print(self.name, " is removed." )

    def add_topic(self, topic) :
        self.topic.append(topic)
        print(self.name, " add topic ", self.topic)

    def add_mess(self, mess):
        self.mess.append(mess)
        print(self.name, " send message, topic :", mess.topic," message :", mess.mess)

class sub :
    name = ""
    topic = []
    message = []
    def __init__ (self, name, topic) :
        self.name = name
        self.topic = []
        self.mess =[]
        self.topic.append(topic)
        print("subscriber", self.name," is constructed.")
    
    def __del__ (self):
        print(self.name, " is removed." )

    def add_topic(self, topic) :
        self.topic.append(topic)
        print(self.name, " subscribe topic :", self.topic)

    def add_mess(self, mess):
        self.mess.append(mess)
        print(self.name, " got message, topic :", mess.topic," message :", mess.mess)

class topic_list :
    def __init__ (self, name) :
        self.name = name
        self.pubs = []
        self.subs = []
        print("topic", self.name, "is added")
    
    def __del__ (self) :
        print("topic list", self.name, " is removed")

    def add_sub(self, sub) :
        self.subs.append(sub)
        print("sub", sub, " topic :", self.name)
    
    def add_pub(self, pub) :
        self.pubs.append(pub)
        print("publisher", sub, " topic :", self.name)

class message :
    def __init__ (self, topic, mess):
        self.topic = topic
        self.mess = mess
  
pubs = []
subs = []
topics = []
messageque = Queue.Queue()

@app.route('/')
def pubsub():
    
#
#     retrieveMessage() : to fill up the messageQue
#
    
    while not messageque.empty():
        temp = messageque.get()
        notify(temp)
    
    return render_template('pubsub.html', pubs = pubs, subs = subs)

@app.route('/regpub')       # add publisher
def regpub() :
     return render_template('regpub.html')

@app.route('/regsub')       # add subscriber
def regsub() :
     return render_template('regsub.html')

# functions

@app.route('/addPub',methods=['POST'])
def addPub():
    #code for access database
    _name = request.form['inputTitle']
    _description = request.form['inputDescription']
    if(_name == "") or (_description=="") :
        return redirect('/')
    else :
        newpub = pub(_name, _description)
        pubs.append(newpub)

        # about topic
        j = 0
        for topic in topics:                  # chech whether topic is exist or not
            if (topic.name == _description) : # when topic is existed,
                topic.add_pub(_name)          #     put the pub_name to the existed topic 
                break
            j = j+1

        if (j == len(topics)):               # when topic is not exsited,
            l = topic_list(_description)     #      make topic_list
            l.add_pub(_name)                 #      put the pub name to topic_list
            topics.append(l)                 #      push new topic to topic containers

        return redirect('/')

@app.route('/addSub',methods=['POST'])
def addSub():
    #code for access database
    _name = request.form['inputTitle']
    _description = request.form['inputDescription']
    if(_name == "" or (_description=="")) :
        return redirect('/')
    else :
        newsub = sub(_name, _description)
        subs.append(newsub)

        # about topic
        j = 0
        for topic in topics:                  # chech whether topic is exist or not
            if (topic.name == _description) : # when topic is existed,
                topic.add_sub(_name)          #     put the sub_name to the existed topic 
                break
            j = j+1

        if (j == len(topics)):                # when topic is not exsited,
            l = topic_list(_description)     #      make topic_list
            l.add_sub(_name)                 #      put the sub name to topic_list
            topics.append(l)                 #      push new topic to topic containers

        return redirect('/')

@app.route('/Advertise',methods=['POST'])
def advertise():                            # advertise topic
    _name = request.form['name']
    _description = request.form['newTopic']

    if(_description == "") :
        return redirect('/')

    for pub in pubs:                     # in pubs list find the pub whose name is _name
        if (pub.name == _name) :         # if find at the pub
            pub.add_topic(_description)  # push the topic to pub's topic array

            j = 0
            for topic in topics:                  # chech whether topic is exist or not
                if (topic.name == _description) : # when topic is existed,
                    topic.add_pub(_name)          #     put the pub_name to the existed topic 
                    break
                j = j+1

            if (j == len(topics)):                # when topic is not exsited,
                l = topic_list(_description)     #      make topic_list
                l.add_pub(_name)                 #      put the pub name to topic_list
                topics.append(l)                 #      push new topic to topic containers
            break

    return redirect('/')

@app.route('/Publish',methods=['POST'])
def publish():
    _name = request.form['name']
    _mess = request.form['message']

    if(_mess == "") :
        return redirect('/')

    #find the pub's information
    for pub in pubs :
        if (pub.name == _name) :
        # save in the pub's message container
            for topic in pub.topic : 
                m = message(topic,_mess) 
                pub.add_mess(m)
                messageque.put(m)
#
#               savetoMessageFile()
#

    return redirect('/')

@app.route('/Subscribe',methods=['POST'])
def subscribe():
    _name = request.form['name']
    _description = request.form['newTopic']

    if(_description == "") :
        return redirect('/')

    for sub in subs:                     # in pubs list find the pub whose name is _name
        if (sub.name == _name) :         # if find at the pub
            sub.add_topic(_description)  # push the topic to pub's topic array

            j = 0
            for topic in topics:                  # chech whether topic is exist or not
                if (topic.name == _description) : # when topic is existed,
                    topic.add_sub(_name)          #     put the pub_name to the existed topic 
                    break
                j = j+1

            if (j == len(topics)):                # when topic is not exsited,
                l = topic_list(_description)     #      make topic_list
                l.add_sub(_name)                 #      put the pub name to topic_list
                topics.append(l)                 #      push new topic to topic containers
            break

    return redirect('/')                

def notify(m):
# save in the subscriber's message container
    topic = m.topic
    for tp in topics :                  # find topic list which is object that the publusher sends message
        if(tp.name == topic):

            for subc in tp.subs :       # find subcribers name of topic (subc)
                for sub in subs :
                    if (sub.name == subc):  # find instace of subscribers
                        sub.add_mess(m)               
    print("server sent message topic :", topic, " message ", m.mess)

def retrieveMessage():

def savetoMessageFile():


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug = True)
