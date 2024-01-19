"""Authentication service application."""

import logging
import sys
from typing import List
import threading
import time

import Ice

import IceDrive
import IceStorm

from .directory import DirectoryService
from .discovery import Discovery


class DirectoryApp(Ice.Application):
    """Implementation of the Ice.Application for the Authentication service."""

    def run(self, args: List[str]) -> int:
        """Setup IceStorm"""
        properties = self.communicator().getProperties()
        topic_name = properties.getProperty("DiscoveryTopic")
        topic_manager = IceStorm.TopicManagerPrx.checkedCast(self.communicator().propertyToProxy("IceStorm.TopicManager.Proxy"))

        try:
            topic = topic_manager.retrieve(topic_name)
        except IceStorm.NoSuchTopic:
            topic = topic_manager.create(topic_name)

        discovery_pub = IceDrive.DiscoveryPrx.uncheckedCast(topic.getPublisher())

        """Execute the code for the AuthentacionApp class."""
        adapter = self.communicator().createObjectAdapter("DirectoryAdapter")
        adapter.activate()

        discovery = Discovery()
        discovery_proxy = adapter.addWithUUID(discovery)

        servant = DirectoryService(discovery)
        servant_proxy = adapter.addWithUUID(servant)

        logging.info("Proxy: %s", servant_proxy)

        directory_proxy = IceDrive.DirectoryServicePrx.uncheckedCast(servant_proxy)

        announce_thread = threading.Thread(target=self.sendAnnouncement, args= (discovery_pub, directory_proxy), daemon=True)
        announce_thread.start()

        

        """Suscripcion al topic"""

        topic.subscribeAndGetPublisher({}, discovery_proxy)
        

        self.shutdownOnInterrupt()
        self.communicator().waitForShutdown()

        return 0

    def sendAnnouncement(self, publisher, servicePrx):
            while True:
                publisher.announceDirectoryService(servicePrx)
                time.sleep(5)

def main():
    """Handle the icedrive-authentication program."""
    app = DirectoryApp()
    return app.main(sys.argv)