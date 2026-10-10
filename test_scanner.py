import unittest

from scanner import is_real_device, parse_devices

SAMPLE_ARP_TEXT = """
Interface: 192.168.1.20 --- 0x5
  Internet Address      Physical Address      Type
  192.168.1.1           A4-83-E7-12-9B-01     dynamic
  192.168.1.255         ff-ff-ff-ff-ff-ff     static
  224.0.0.22            01-00-5e-00-00-16     static
"""


class TestParseDevices(unittest.TestCase):
    def test_finds_every_row(self):
        devices = parse_devices(SAMPLE_ARP_TEXT)
        self.assertEqual(len(devices), 3)

    def test_reads_ip_and_mac(self):
        first = parse_devices(SAMPLE_ARP_TEXT)[0]
        self.assertEqual(first["ip"], "192.168.1.1")
        self.assertEqual(first["mac"], "a4-83-e7-12-9b-01")

    def test_empty_text_gives_no_devices(self):
        self.assertEqual(parse_devices(""), [])


class TestIsRealDevice(unittest.TestCase):
    def test_normal_device_is_real(self):
        device = {"ip": "192.168.1.1", "mac": "a4-83-e7-12-9b-01"}
        self.assertTrue(is_real_device(device))

    def test_broadcast_is_not_real(self):
        device = {"ip": "192.168.1.255", "mac": "ff-ff-ff-ff-ff-ff"}
        self.assertFalse(is_real_device(device))

    def test_multicast_is_not_real(self):
        device = {"ip": "224.0.0.22", "mac": "01-00-5e-00-00-16"}
        self.assertFalse(is_real_device(device))


if __name__ == "__main__":
    unittest.main()