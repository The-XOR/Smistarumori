import supervisor
import storage
supervisor.set_usb_identification("The XOR", "Smistarumori")

storage.remount("/", readonly=False)
m = storage.getmount("/")
m.label = "SMISTARUMOR"
# Enable USB mass storage
storage.remount("/", readonly=False)
storage.enable_usb_drive()

# Disable USB mass storage
# storage.disable_usb_drive()
# storage.remount("/", readonly=True)
