# -*- coding: utf-8 -*-
"""Standardized log messages module.
"""


from enum import Enum


class LogMessage(Enum):
    """Standardized log messages enumeration."""

    UNEXPECTEDEXCEPTION = 'f"Unexpected exception: {err}. Exception type {type(err)}."'
    AGENTALREADYCONNECTED = 'f"Agent {agent_id} already connected to {self.unique_id}."'
    NEWAGENTACONNECTED = 'f"Agent {agent_id} connected with {self.unique_id}."'
    NEWAGENTREMOVED = 'f"Agent {agent_id} disconnected with {self.unique_id}."'
    AGENTNOTFOUND = 'f"Agent {agent_id} not found."'
