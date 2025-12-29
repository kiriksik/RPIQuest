class ProjectorController:
    def update(self, pin_state):
        if pin_state:
            send("projectorOn")
            relay.on()
        else:
            send("projectorOff")
            relay.off()
