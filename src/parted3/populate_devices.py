#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  populate_devices.py
#
#  Copyright © 2013-2017 Antergos
#
#  This file is part of Cnchi.
#
#  Cnchi is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  Cnchi is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  The following additional terms are in effect as per Section 7 of the license:
#
#  The preservation of all legal notices and author attributions in
#  the material or in the Appropriate Legal Notices displayed
#  by works containing it is required.
#
#  You should have received a copy of the GNU General Public License
#  along with Cnchi; If not, see <http://www.gnu.org/licenses/>.


""" Get devices and parititons information in a str list """

import logging
import parted
import misc.extra as misc

@misc.raise_privileges
def populate_devices(do_partitions=False):
    """ Fill str list with all devices (and partitions if desired) """
    try:
        device_list = parted.getAllDevices()
    except parted._ped.DiskException as warn:
        logging.warning(warn)

    devices = {}

    if do_partitions:
        devices['None'] = (None, None)

    for dev in device_list:
        if dev.path.startswith("/dev/sr") or dev.path.startswith("/dev/mapper"):
            # avoid cdrom and any raid, lvm volumes or encryptfs
            continue
        # hard drives measure themselves assuming kilo=1000, mega=1mil, etc
        size = dev.length * dev.sectorSize
        size_gbytes = int(parted.formatBytes(size, 'GB'))
        line = "{0} [{1} GB] ({2})"
        line = line.format(dev.model, size_gbytes, dev.path)
        if do_partitions:
            devices[line] = (dev.path, None)
            devices.update(populate_partitions(dev))
        else:
            devices[line] = dev.path
        logging.debug(line)
    return devices


@misc.raise_privileges
def populate_partitions(dev):
    """ Fill str list with all device's partitions """
    partitions = {}
    try:
        disk = parted.newDisk(dev)
        for partition in disk.partitions:
            if partition.type in [parted.PARTITION_NORMAL, parted.PARTITION_LOGICAL]:
                size = partition.geometry.length * dev.sectorSize
                size_gbytes = int(parted.formatBytes(size, 'GB'))
                if size_gbytes > 0:
                    line = "\t{0} [{1} GB]"
                    line = line.format(partition.path, size_gbytes)
                    partitions[line] = (dev.path, partition.path)
    except parted._ped.DiskException as warn:
        # It could be that the device has no partition table
        logging.warning(warn)
    return partitions
