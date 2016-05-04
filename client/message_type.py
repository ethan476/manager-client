from enum import Enum;

class MessageType(Enum):
	PING = 0;
	PONG = 1;
	REQUEST = 2;
	RESPONSE = 3;
	TRIGGER_PUSH = 4;
