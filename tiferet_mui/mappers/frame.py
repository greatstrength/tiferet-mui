"""Tiferet MUI Frame Mappers"""

# *** imports

# ** core
from typing import Any, ClassVar, Dict

# ** app
from tiferet.mappers import TransferObject

from ..domain import Frame

# *** mappers

# ** mapper: frame_transfer_object
class FrameTransferObject(Frame, TransferObject):
    '''
    Converts a frame into the JSON-safe recursive props tree the binding passes
    to the frontend, while retaining a direct path back to the domain shape.
    '''

    # * attribute: _ROLES
    _ROLES: ClassVar[Dict[str, Dict[str, Any]]] = {
        'to_model': {},
        'to_data': {
            'mode': 'json',
        },
    }

    # * method: map
    def map(self, **overrides) -> Frame:
        '''
        Map the serialized frame data to its domain representation.

        :param overrides: Additional field values that override serialized data.
        :type overrides: dict
        :return: The mapped frame domain object.
        :rtype: Frame
        '''

        # Construct the domain frame through the shared transfer-object path.
        return super().map(Frame, **overrides)

    # * method: from_model
    @classmethod
    def from_model(cls, frame: Frame, **overrides) -> 'FrameTransferObject':
        '''
        Create a transfer object from a composed frame.

        :param frame: The composed frame domain object.
        :type frame: Frame
        :param overrides: Additional field values that override model data.
        :type overrides: dict
        :return: The frame transfer object.
        :rtype: FrameTransferObject
        '''

        # Convert the domain frame through the shared transfer-object path.
        return super().from_model(frame, **overrides)
