import pjsua as pj
import time

# Define account and server details
SIP_DOMAIN = "192.168.192.100"
SIP_USER = "hFjr9AqEj1"
SIP_PASSWD = "wovPFv2umi"
SIP_EXTENSION = "sip:000@" + SIP_DOMAIN
WAV_FILE = "announcment.wav"

# Callback to handle events
class MyAccountCallback(pj.AccountCallback):
    def __init__(self, account):
        pj.AccountCallback.__init__(self, account)

class MyCallCallback(pj.CallCallback):
    def __init__(self, call):
        pj.CallCallback.__init__(self, call)
    
    def on_state(self):
        print("Call is", self.call.info().state_text, "last code =", self.call.info().last_code, "(" + self.call.info().last_reason + ")")
        if self.call.info().state == pj.CallState.DISCONNECTED:
            print("Call disconnected")
            self.call.hangup()

    def on_media_state(self):
        if self.call.info().media_state == pj.MediaState.ACTIVE:
            # Get the media transport
            call_slot = self.call.info().conf_slot
            # Play the wav file
            wav_player_id = pj.Lib.instance().create_player(WAV_FILE, loop=False)
            wav_slot = pj.Lib.instance().player_get_slot(wav_player_id)
            pj.Lib.instance().conf_connect(wav_slot, call_slot)
            print("Media is now active")
        else:
            print("Media is inactive")

# Initialize the library
lib = pj.Lib()

try:
    lib.init(log_cfg = pj.LogConfig(level=3, callback=None))
    lib.create_transport(pj.TransportType.UDP, pj.TransportConfig(5060))
    lib.start()

    # Create and register account
    acc_cfg = pj.AccountConfig(SIP_DOMAIN, SIP_USER, SIP_PASSWD)
    acc = lib.create_account(acc_cfg, cb=MyAccountCallback)

    # Make call to the extension
    call = acc.make_call(SIP_EXTENSION, cb=MyCallCallback)

    # Keep the application running until the call ends
    while call.info().state != pj.CallState.DISCONNECTED:
        time.sleep(1)

finally:
    lib.destroy()
    lib = None
