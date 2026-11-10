# ************************************************************
# File name: dabble_ble_server.py
# Purpose: Dabble BLE GATT Server for Orange Pi
# Operating System: Ubuntu Linux
# Future integration: ROS 2
# ************************************************************

import sys

from dabble_bluetooth import DabbleReceiver


# Dabble Bluetooth configuration
DEVICE_NAME = "OrangePi_Dabble"

SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
RX_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
TX_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"


# BlueZ interfaces
BLUEZ = "org.bluez"
GATT_MANAGER = "org.bluez.GattManager1"
ADV_MANAGER = "org.bluez.LEAdvertisingManager1"

GATT_SERVICE = "org.bluez.GattService1"
GATT_CHARACTERISTIC = "org.bluez.GattCharacteristic1"

ADVERTISEMENT = "org.bluez.LEAdvertisement1"
PROPERTIES = "org.freedesktop.DBus.Properties"
OBJECT_MANAGER = "org.freedesktop.DBus.ObjectManager"


# Our existing Dabble receiver
receiver = DabbleReceiver()


def on_ble_data(data):

    print("BLE received:", data.hex(" ").upper())

    receiver.receive_data(data)


def main():

    # BlueZ server requires Ubuntu/Linux
    if sys.platform != "linux":

        print("This program must run on Ubuntu Linux.")
        return

    # Import Linux Bluetooth libraries
    try:
        import dbus
        import dbus.service
        import dbus.mainloop.glib

        from gi.repository import GLib

    except ImportError as error:

        print("Missing Linux Bluetooth dependency:", error)
        return

    # Initialize D-Bus
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    bus = dbus.SystemBus()
    loop = GLib.MainLoop()

    APP_PATH = "/com/orangepi/dabble"
    SERVICE_PATH = APP_PATH + "/service0"
    RX_PATH = SERVICE_PATH + "/char0"
    TX_PATH = SERVICE_PATH + "/char1"
    ADV_PATH = APP_PATH + "/advertisement0"

    # --------------------------------------------------------
    # GATT Application
    # --------------------------------------------------------

    class Application(dbus.service.Object):

        def __init__(self):
            super().__init__(bus, APP_PATH)

        @dbus.service.method(
            OBJECT_MANAGER,
            out_signature="a{oa{sa{sv}}}"
        )
        def GetManagedObjects(self):

            return {
                SERVICE_PATH: {
                    GATT_SERVICE: service_properties()
                },
                RX_PATH: {
                    GATT_CHARACTERISTIC: rx_properties()
                },
                TX_PATH: {
                    GATT_CHARACTERISTIC: tx_properties()
                }
            }

    # --------------------------------------------------------
    # GATT Service
    # --------------------------------------------------------

    def service_properties():

        return {
            "UUID": SERVICE_UUID,
            "Primary": dbus.Boolean(True),
            "Includes": dbus.Array([], signature="o")
        }

    class DabbleService(dbus.service.Object):

        def __init__(self):
            super().__init__(bus, SERVICE_PATH)

        @dbus.service.method(
            PROPERTIES,
            in_signature="s",
            out_signature="a{sv}"
        )
        def GetAll(self, interface):

            if interface != GATT_SERVICE:
                raise ValueError("Unknown interface")

            return service_properties()

    # --------------------------------------------------------
    # RX Characteristic: iPhone -> Orange Pi
    # --------------------------------------------------------

    def rx_properties():

        return {
            "UUID": RX_UUID,
            "Service": dbus.ObjectPath(SERVICE_PATH),
            "Flags": dbus.Array(["write"], signature="s")
        }

    class RXCharacteristic(dbus.service.Object):

        def __init__(self):
            super().__init__(bus, RX_PATH)

        @dbus.service.method(
            PROPERTIES,
            in_signature="s",
            out_signature="a{sv}"
        )
        def GetAll(self, interface):

            if interface != GATT_CHARACTERISTIC:
                raise ValueError("Unknown interface")

            return rx_properties()

        @dbus.service.method(
            GATT_CHARACTERISTIC,
            in_signature="aya{sv}",
            out_signature=""
        )
        def WriteValue(self, value, options):

            data = bytes(value)

            on_ble_data(data)

    # --------------------------------------------------------
    # TX Characteristic: Orange Pi -> iPhone
    # --------------------------------------------------------

    def tx_properties():

        return {
            "UUID": TX_UUID,
            "Service": dbus.ObjectPath(SERVICE_PATH),
            "Flags": dbus.Array(["notify"], signature="s")
        }

    class TXCharacteristic(dbus.service.Object):

        def __init__(self):
            super().__init__(bus, TX_PATH)
            self.notifying = False

        @dbus.service.method(
            PROPERTIES,
            in_signature="s",
            out_signature="a{sv}"
        )
        def GetAll(self, interface):

            return tx_properties()

        @dbus.service.method(
            GATT_CHARACTERISTIC,
            in_signature="",
            out_signature=""
        )
        def StartNotify(self):

            self.notifying = True
            print("Notifications enabled")

        @dbus.service.method(
            GATT_CHARACTERISTIC,
            in_signature="",
            out_signature=""
        )
        def StopNotify(self):

            self.notifying = False
            print("Notifications disabled")

    # --------------------------------------------------------
    # BLE Advertisement
    # --------------------------------------------------------

    class DabbleAdvertisement(dbus.service.Object):

        def __init__(self):
            super().__init__(bus, ADV_PATH)

        @dbus.service.method(
            PROPERTIES,
            in_signature="s",
            out_signature="a{sv}"
        )
        def GetAll(self, interface):

            if interface != ADVERTISEMENT:
                raise ValueError("Unknown interface")

            return {
                "Type": "peripheral",
                "ServiceUUIDs": dbus.Array(
                    [SERVICE_UUID], signature="s"
                ),
                "LocalName": DEVICE_NAME
            }

        @dbus.service.method(
            ADVERTISEMENT,
            in_signature="",
            out_signature=""
        )
        def Release(self):

            print("Advertisement released")

    # --------------------------------------------------------
    # Communication watchdog
    # --------------------------------------------------------

    def check_connection():

        receiver.check_timeout()

        return True

    # --------------------------------------------------------
    # Register Bluetooth services
    # --------------------------------------------------------

    app = Application()
    service = DabbleService()
    rx = RXCharacteristic()
    tx = TXCharacteristic()
    advertisement = DabbleAdvertisement()

    adapter_path = "/org/bluez/hci0"

    adapter = bus.get_object(BLUEZ, adapter_path)

    gatt_manager = dbus.Interface(adapter, GATT_MANAGER)
    adv_manager = dbus.Interface(adapter, ADV_MANAGER)

    def on_error(error):

        print("Bluetooth registration failed:", error)
        receiver.disconnect()
        loop.quit()

    def on_advertisement_ready():

        print("BLE advertising started!")
        print("Device name:", DEVICE_NAME)
        print("Waiting for Dabble connection...")

    def on_application_ready():

        print("GATT application registered")

        adv_manager.RegisterAdvertisement(
            ADV_PATH,
            {},
            reply_handler=on_advertisement_ready,
            error_handler=on_error
        )

    gatt_manager.RegisterApplication(
        APP_PATH,
        {},
        reply_handler=on_application_ready,
        error_handler=on_error
    )

    # Check communication every 100 milliseconds
    GLib.timeout_add(100, check_connection)

    print("Starting Dabble BLE Server...")

    try:
        loop.run()

    except KeyboardInterrupt:
        print("Stopping Bluetooth server...")

    finally:
        receiver.disconnect()


# Main program
if __name__ == "__main__":
    main()