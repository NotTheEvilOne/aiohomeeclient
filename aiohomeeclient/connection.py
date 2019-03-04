# -*- coding: utf-8 -*-

"""
(C) Tobias Wolf et al. - All rights reserved

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
"""

from concurrent.futures import TimeoutError as FutureTimeoutError
from hashlib import sha512
from json import loads as parseJson
from time import time
from urllib.parse import quote_plus
import asyncio
import sys

from aiohttp import ClientSession, ClientTimeout, WSMsgType

from .registry import Registry
from .node import Node

class Connection(object):
    """
The "Connection" class provides the asynchronous API to communicate with the
homee brain.

:author:     Tobias Wolf et al.
:copyright:  Tobias Wolf et al. - All rights reserved
:package:    aiohomee
:subpackage: client
:since:      1.0.0
:license:    Mozilla Public License, v. 2.0
    """

    API_MESSAGE_TIMEOUT = 0.25
    """
Timeout in seconds to wait for a message.
    """
    IO_TIMEOUT = 5
    """
Timeout in seconds for communication.
    """
    TOKEN_TIMEOUT_THRESHOLD = 30
    """
Threshold in seconds before a token expires to request a new one.
    """
    WS_LOCAL_PORT = 7681
    """
Local homee websocket port
    """

    def __init__(self, address, username, password):
        """
Constructor __init__(Connection)

:since: 1.0.0
        """

        self.address = address
        """
homee address to connect to
        """
        self._address_is_local = (".hom.ee" not in address)
        """
True if the given homee address is not the remote proxy one
        """
        self._client_session = None
        """
aiohttp client session instance
        """
        self.password = password
        """
homee user password
        """
        self._registry = None
        """
Nodes registry connected to this instance
        """
        self._socket = None
        """
homee connection websocket
        """
        self._token = None
        """
Authorized homee access token
        """
        self._token_timeout = 0
        """
Authorized homee access token timeout
        """
        self.username = username
        """
homee user name
        """
    #

    async def __aenter__(self):
        """
Enter the runtime context related to this object. It must return an
awaitable.

:since: 1.0.0
        """

        if (self._socket is None or self._socket.closed):
            await self.connect()
        #

        await self._handle_messages()
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

    def __getattribute__(self, name):
        """
python.org: Called unconditionally to implement attribute accesses for
instances of the class.

:param name: Attribute name

:return: (mixed) Instance attribute
:since:  1.0.0
        """

        """
The following list of attributes are filtered either for performance reasons
or to catch recursion.
        """

        if (name not in ("access_token",
                         "address",
                         "_address_is_local",
                         "__aexit__",
                         "__class__",
                         "_client_session",
                         "connect",
                         "disconnect",
                         "_handle_message",
                         "_handle_messages",
                         "is_connected",
                         "location",
                         "password",
                         "_socket",
                         "_token",
                         "_token_timeout",
                         "username"
                        )
            and (self._socket is None or self._socket.closed)
           ): raise IOError("Connection has not been established or has been closed")
        #

        return object.__getattribute__(self, name)
    #

    @property
    async def access_token(self):
        """
Returns the authorized access token.

:return: (str) Authorized homee access token
:since:  1.0.0
        """

        if (self._client_session is None): raise IOError("Connection has not been established")

        if (self._token is None or time() > self._token_timeout):
            protocol = ("http" if (self._address_is_local) else "https")

            os_value = 0

            if (sys.platform == "darwin"): os_value = 6
            elif (sys.platform == "linux"): os_value = 5
            elif (sys.platform in ( "cygwin", "win32" )): os_value = 3

            data = {
                "device_name": "aiohomeeclient",
                "device_hardware_id": "aiohomeeclient",
                "device_os": os_value,
                "device_type": 3,
                "device_app": 1
            }

            username = quote_plus(self.username)
            password = sha512(self.password.encode("utf-8")).hexdigest()
            url = "{0}://{1}:{2}@{3}/access_token".format(protocol, username, password, self.location)

            response = await self._client_session.post(url, data = data)

            expires = (1 + Connection.TOKEN_TIMEOUT_THRESHOLD
                       if (response.cookies['access_token']['max-age'] == "") else
                       int(response.cookies['access_token']['max-age'])
                      )

            self._token = response.cookies['access_token'].value
            self._token_timeout = time() + (expires - Connection.TOKEN_TIMEOUT_THRESHOLD)
        #

        return self._token
    #

    @property
    def is_connected(self):
        """
Returns true if the connection is ready.

:return: (bool) True if ready
:since:  1.0.0
        """

        return (self._socket is not None and (not self._socket.closed))
    #

    @property
    def location(self):
        """
Returns the URL base location for communication with homee.

:return: (str) URL base location
:since:  1.0.0
        """

        port = (":{0:d}".format(self.__class__.WS_LOCAL_PORT) if (self._address_is_local) else "")
        return "{0}{1}".format(self.address, port)
    #

    @property
    def registry(self):
        """
Returns the nodes registry connected to this instance.

:return: (object) Nodes registry instance
:since:  1.0.0
        """

        if (self._registry is None): self._registry = Registry(self)
        return self._registry
    #

    async def connect(self):
        """
Establishes a connection to homee.

:since: 1.0.0
        """

        self._client_session = ClientSession(raise_for_status = True,
                                             timeout = ClientTimeout(total = self.__class__.IO_TIMEOUT)
                                            )

        protocol = ("ws" if (self._address_is_local) else "wss")
        token = quote_plus(await self.access_token)

        headers = { "Accept-Charset": "utf-8" }
        url = "{0}://{1}/connection?access_token={2}".format(protocol, self.location, token)

        self._socket = await self._client_session.ws_connect(url,
                                                             headers = headers,
                                                             protocols = [ "v2" ]
                                                            )
    #

    async def disconnect(self):
        """
Disconnects from homee.

:since: 1.0.0
        """

        self._registry = None

        await self._socket.close()
        self._socket = None

        await self._client_session.close()
        self._client_session = None
    #

    async def _handle_message(self, message):
        """
Handles a message received from the homee websocket connection.

:param message: Message dictionary

:since: 1.0.0
        """

        if (type(message) is not dict or len(message) != 1): raise RuntimeError("Unsupported format detected in API message stream: {0}".format(message))

        if ("attribute" in message):
            self.registry.update_node_attribute(message['attribute']['node_id'],
                                                message['attribute']['id'],
                                                message['attribute']
                                               )
        elif ("attribute_history" in message and type(message['attribute_history']) is dict):
            pass
        elif ("all" in message and type(message['all']) is dict):
            for type_key in message['all']:
                await self._handle_message(dict([ ( type_key, message['all'][type_key] ) ]))
            #
        elif ("groups" in message and type(message['groups']) is list):
            pass
        elif ("homeegram_history" in message and type(message['homeegram_history']) is dict):
            pass
        elif ("homeegrams" in message and type(message['homeegrams']) is list):
            pass
        elif ("node" in message and type(message['node']) is dict):
            self.registry.add_or_update_node(Node.from_dict(message['node'], self))
        elif ("node_history" in message and type(message['node_history']) is dict):
            pass
        elif ("nodes" in message and type(message['nodes']) is list):
            for node in message['nodes']:
                await self._handle_message(dict([ ( "node", node ) ]))
            #
        elif ("plans" in message and type(message['plans']) is list):
            pass
        elif ("relationships" in message and type(message['relationships']) is list):
            pass
        elif ("settings" in message and type(message['settings']) is dict):
            pass
        elif ("users" in message and type(message['users']) is list):
            pass
        else: raise RuntimeError("Unsupported format detected in API message stream: {0}".format(message))
    #

    async def receive_and_handle_messages(self, timeout = None):
        """
Handles all pending messages from the homee websocket connection.

:param is_response_expected: True if an API response is expected

:since: 1.0.0
        """

        try:
            timeout_remaining = (0 if (timeout is None) else timeout)

            while True:
                if (timeout == 0): message = await self._socket.receive()
                else:
                    time_started = time()

                    receive_timeout = (timeout_remaining
                                       if (timeout_remaining > 0) else
                                       self.__class__.API_MESSAGE_TIMEOUT
                                      )

                    message = await self._socket.receive(timeout = receive_timeout)

                    if (timeout_remaining > 0): timeout_remaining -= time() - time_started
                #

                if message.type == WSMsgType.CLOSED: break
                elif message.type == WSMsgType.ERROR: raise RuntimeError(message.data)
                elif message.type == WSMsgType.TEXT: await self._handle_message(parseJson(message.data))
            #
        except FutureTimeoutError: pass
    #

    async def send(self, request):
        """
Sends the given request to the homee API.

:param request: homee API request

:since: 1.0.0
        """

        await self._socket.send_str(request)
    #
#
