provides = "temp"
import random, sys
def get_value(server_request=None):
    return random.randrange(30,40)
def trigger_called(trigger):
    return get_value()
if __name__ == "main":
    print("Fuck off")
    sys.exit(1)
