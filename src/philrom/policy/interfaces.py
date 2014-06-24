# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from recensio.theme.interfaces import IRecensioLayer


class IPhilromLayer(IRecensioLayer):
    """Marker interface that defines a Zope 3 browser layer."""
