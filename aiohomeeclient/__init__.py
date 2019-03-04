# -*- coding: utf-8 -*-

"""
(C) Tobias Wolf et al. - All rights reserved

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
"""

from weakref import proxy

from .connection import Connection

class Homee(object):
    """
The "Homee" class is the main entry point to communicate with a homee.

:author:     Tobias Wolf et al.
:copyright:  Tobias Wolf et al. - All rights reserved
:package:    aiohomee
:subpackage: client
:since:      1.0.0
:license:    Mozilla Public License, v. 2.0
    """

    API_RESPONSE_TIMEOUT = 1
    """
Timeout in seconds to wait for an expected API response.
    """

    def __init__(self, address, username, password):
        """
Constructor __init__(Connection)

:since: 1.0.0
        """

        self._connection = Connection(address, username, password)
        """
homee connection
        """
    #

    async def __aenter__(self):
        """
Enter the runtime context related to this object. It must return an
awaitable.

:since: 1.0.0
        """

        if (not self._connection.is_connected): await self.connect()
    #

    async def __aexit__(self, exc_type, exc_value, traceback):
        """
Exit the runtime context related to this object. It must return an
awaitable.

:return: (bool) True to suppress exceptions
:since:  1.0.0
        """

        return False
    #

    @property
    def _registry(self):
        """
Returns the nodes registry connected to this instance.

:return: (object) Nodes registry instance
:since:  1.0.0
        """

        return self._connection.registry
    #

    async def connect(self):
        """
Establishes a connection to homee.

:since: 1.0.0
        """

        await self._connection.connect()
        await self.refreshAll()
    #

    async def disconnect(self):
        """
Disconnects from homee.

:since: 1.0.0
        """

        await self._connection.disconnect()
    #

    async def get_node(self, node_name_or_id):
        """
Returns the node for the ID given.

:param node_name_or_id: homee node ID or name

:return: (object) Node instance
:since:  1.0.0
        """

        async with self:
            node_id = (node_name_or_id
                       if (type(node_name_or_id) is int) else
                       self._registry.get_node_id_for_name(node_name_or_id)
                      )

            return self._registry.get_node(node_id)
        #
    #

    async def is_node_known(self, node_name_or_id):
        """
Returns true if the node ID given is registered.

:param node_name_or_id: homee node ID or name

:return: (bool) True if known
:since:  1.0.0
        """


        async with self:
            node_id = (node_name_or_id
                       if (type(node_name_or_id) is int) else
                       self._registry.get_node_id_for_name(node_name_or_id)
                      )

            return self._registry.is_node_known(node_id)
        #
    #

    async def refreshAll(self):
        """
Refreshes all data types exposed by the homee API.

:since: 1.0.0
        """

        await self.send_and_receive_messages("GET:all")
    #

    async def refreshGroups(self):
        """
Refreshes all groups exposed by the homee API.

:since: 1.0.0
        """

        await self.send_and_receive_messages("GET:groups")
    #

    async def refreshHomeegrams(self):
        """
Refreshes all homeegrams exposed by the homee API.

:since: 1.0.0
        """

        await self.send_and_receive_messages("GET:homeegrams")
    #

    async def refreshNodes(self):
        """
Refreshes all nodes exposed by the homee API.

:since: 1.0.0
        """

        await self.send_and_receive_messages("GET:nodes")
    #

    async def refreshPlans(self):
        """
Refreshes all plans exposed by the homee API.

:since: 1.0.0
        """

        await self.send_and_receive_messages("GET:plans")
    #

    async def refreshRelationships(self):
        """
Refreshes all data relationships exposed by the homee API.

:since: 1.0.0
        """

        await self.send_and_receive_messages("GET:relationships")
    #

    async def refreshSettings(self):
        """
Refreshes all settings exposed by the homee API.

:since: 1.0.0
        """

        await self.send_and_receive_messages("GET:settings")
    #

    async def refreshUsers(self):
        """
Refreshes all users exposed by the homee API.

:since: 1.0.0
        """

        await self.send_and_receive_messages("GET:users")
    #

    async def send(self, request):
        """
Sends the given request to the homee API.

:param request: homee API request

:since: 1.0.0
        """

        async with self: await self._connection.send(request)
    #

    async def send_and_receive_messages(self, request):
        """
Sends the given request to the homee API and wait for responses.

:param request: homee API request

:since: 1.0.0
        """

        async with self:
            await self.send(request)
            await self._connection.receive_and_handle_messages(self.__class__.API_RESPONSE_TIMEOUT)
        #
    #
#
