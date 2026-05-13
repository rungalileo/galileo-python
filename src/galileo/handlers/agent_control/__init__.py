"""Agent Control bridge for Galileo logger-backed control span ingestion.

For Agent Control target resolution, use ``galileo.agent_control``.
"""

from galileo.handlers.agent_control.bridge import GalileoAgentControlBridge, setup_agent_control_bridge

__all__ = ["GalileoAgentControlBridge", "setup_agent_control_bridge"]
