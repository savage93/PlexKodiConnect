#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from .. import utils


def remove_trailing_slash(path):
    """
    Removes trailing slashes or backslashes from path [unicode], and is NOT
    dependent on os.path
    """
    if '/' in path:
        path = path[:-1] if path.endswith('/') else path
    else:
        path = path[:-1] if path.endswith('\\') else path
    return path


class Sync(object):
    def __init__(self, entrypoint=False):
        self.load()
        # Do we need to run a special library scan?
        self.run_lib_scan = None
        # Set if user decided to cancel sync
        self.stop_sync = False
        # Set during media playback if PKC should not do any syncs. Will NOT
        # suspend synching of playstate progress
        self.suspend_sync = False
        # Could we access the paths?
        self.path_verified = False
        # Set if a Plex-Kodi DB sync is being done - along with
        # window('plex_dbScan') set to 'true'
        self.db_scan = False

    def load(self):
        # Direct Paths (True) or Addon Paths (False)?
        self.direct_paths = utils.settings('useDirectPaths') == '1'
        # Is synching of Plex music enabled?
        self.enable_music = utils.settings('enableMusic') == 'true'
        # Do we sync artwork from the PMS to Kodi?
        self.artwork = utils.settings('usePlexArtwork') == 'true'
        # Path remapping mechanism (e.g. smb paths)
        # Do we replace \\myserver\path to smb://myserver/path?
        self.replace_smb_path = utils.settings('replaceSMB') == 'true'
        # Do we generally remap?
        self.remap_path = utils.settings('remapSMB') == 'true'
        self.force_transcode_pix = utils.settings('force_transcode_pix') == 'true'
        # Mappings for REMAP_PATH:
        self.remapSMBmovieOrg = remove_trailing_slash(utils.settings('remapSMBmovieOrg'))
        self.remapSMBmovieNew = remove_trailing_slash(utils.settings('remapSMBmovieNew'))
        self.remapSMBtvOrg = remove_trailing_slash(utils.settings('remapSMBtvOrg'))
        self.remapSMBtvNew = remove_trailing_slash(utils.settings('remapSMBtvNew'))
        self.remapSMBmusicOrg = remove_trailing_slash(utils.settings('remapSMBmusicOrg'))
        self.remapSMBmusicNew = remove_trailing_slash(utils.settings('remapSMBmusicNew'))
        self.remapSMBphotoOrg = remove_trailing_slash(utils.settings('remapSMBphotoOrg'))
        self.remapSMBphotoNew = remove_trailing_slash(utils.settings('remapSMBphotoNew'))
        # Escape path?
        self.escape_path = utils.settings('escapePath') == 'true'
        # Shall we replace custom user ratings with the number of versions available?
        self.indicate_media_versions = utils.settings('indicate_media_versions') == "true"
        # Will sync movie trailer differently: either play trailer directly or show
        # all the Plex extras for the user to choose
        self.show_extras_instead_of_playing_trailer = utils.settings('showExtrasInsteadOfTrailer') == 'true'
        # Only sync specific Plex playlists to Kodi?
        self.sync_specific_plex_playlists = utils.settings('syncSpecificPlexPlaylists') == 'true'
        # Only sync specific Kodi playlists to Plex?
        self.sync_specific_kodi_playlists = utils.settings('syncSpecificKodiPlaylists') == 'true'
        # Shall we show Kodi dialogs when synching?
        self.sync_dialog = utils.settings('dbSyncIndicator') == 'true'

        # How often shall we sync?
        self.full_sync_intervall = int(utils.settings('fullSyncInterval')) * 60
        # Background Sync disabled?
        self.background_sync_disabled = utils.settings('enableBackgroundSync') == 'false'
        # How long shall we wait with synching a new item to make sure Plex got all
        # metadata?
        self.backgroundsync_saftymargin = int(utils.settings('backgroundsync_saftyMargin'))
        # How many threads to download Plex metadata on sync?
        self.sync_thread_number = int(utils.settings('syncThreadNumber'))

        # Shall Kodi show dialogs for syncing/caching images? (e.g. images left
        # to sync)
        self.image_sync_notifications = utils.settings('imageSyncNotifications') == 'true'
