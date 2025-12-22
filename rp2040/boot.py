import supervisor
import storage
supervisor.set_usb_identification("The XOR", "Smistarumori")

storage.remount("/", readonly=False)
m = storage.getmount("/")
m.label = "SMISTARUMOR"
storage.remount("/", readonly=False)
storage.enable_usb_drive()
