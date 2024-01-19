"""Servant implementations for service discovery."""
import logging
import Ice

import IceDrive


class Discovery(IceDrive.Discovery):
    """Servants class for service discovery."""
    announceAuthentication_set = set()
    announceBlobService_set = set()

    def announceAuthentication(self, prx: IceDrive.AuthenticationPrx, current: Ice.Current = None) -> None:
        """Receive an Authentication service announcement."""
        print("AutProxy: %s", prx)
        self.announceAuthentication_set.add(prx)

    def announceDirectoryService(self, prx: IceDrive.DirectoryServicePrx, current: Ice.Current = None) -> None:
        """Receive an Directory service announcement."""
        print("DirProxy: %s", prx)

    def announceBlobService(self, prx: IceDrive.BlobServicePrx, current: Ice.Current = None) -> None:
        """Receive an Blob service announcement."""
        print("BlobProxy: %s", prx)
        self.announceBlobService_set.add(prx)

    def get_Authentication(self)-> IceDrive.AuthenticationPrx:
        """devuelve un proxy de authentication"""
        while len(self.announceAuthentication_set) > 0:
            prx = self.announceAuthentication_set.pop()
            self.announceAuthentication_set.add(prx)
            try:
                prx.ice_ping()
                return prx
            except Ice.Exception:
                self.announceAuthentication_set.remove(prx)

        return None
                
            
    
    def get_BlobService(self)-> IceDrive.BlobServicePrx:
        """devuelve un proxy del BlobService"""
        while len(self.announceBlobService_set) > 0:
            prx = self.announceBlobService_set.pop()
            self.announceBlobService_set.add(prx)
            try:
                prx.ice_ping()
                return prx
            except Ice.Exception:
                self.announceBlobService_set.remove(prx)

        return None