# -*- coding: utf-8 -*-

"""
osTicket API Client
Copyright (C) SASCO SpA (https://sasco.cl)

Este programa es software libre: usted puede redistribuirlo y/o modificarlo
bajo los términos de la GNU Lesser General Public License (LGPL) publicada
por la Fundación para el Software Libre, ya sea la versión 3 de la Licencia,
o (a su elección) cualquier versión posterior de la misma.

Este programa se distribuye con la esperanza de que sea útil, pero SIN
GARANTÍA ALGUNA; ni siquiera la garantía implícita MERCANTIL o de APTITUD
PARA UN PROPÓSITO DETERMINADO. Consulte los detalles de la GNU Lesser General
Public License (LGPL) para obtener una información más detallada.

Debería haber recibido una copia de la GNU Lesser General Public License
(LGPL) junto a este programa. En caso contrario, consulte
<http://www.gnu.org/licenses/lgpl.html>.
"""

from os import getenv
import requests
import json


# clase para trabajar con la API de osTicket
class osTicket:

    def __init__(self, url = None, api_key = None):
        self.url = str(url if url is not None else getenv('OSTICKET_URL'))
        self.api_key = str(api_key if api_key is not None else getenv('OSTICKET_API_KEY'))

    def ticket_create(self, email, name, subject, message, topicId, attachments = [], ip = None, message_type = 'plain', message_charset = 'utf-8', alert = True, autorespond = True, source = 'API'):
        message = 'data:text/%(type)s;charset=%(charset)s,%(message)s' % {
            'type': message_type,
            'charset': message_charset,
            'message': message,
        }
        ticket = {
            'source': source,
            'email': email,
            'name': name,
            'subject': subject,
            'message': message,
            'ip': str(ip),
            'topicId': topicId,
            'alert': alert,
            'autorespond': autorespond,
            'attachments': attachments,
        }
        response = requests.post(
            '%(url)s/api/http.php/tickets.json' % {'url': self.url},
            data = json.dumps(ticket),
            headers = {
                'X-API-Key': self.api_key
            }
        )
        if response.status_code != 201:
            raise osTicketException(response.content.decode())
        return int(response.content)

# clase para generar la excepción de osticket al usar su API
class osTicketException(Exception):

    def __init__(self, message, code=None, params=None):
        self.message = message
        super().__init__(message, code, params)

    def __str__(self):
        return self.message
