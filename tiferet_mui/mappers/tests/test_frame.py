"""Tiferet MUI Frame Mapper Tests"""

# *** imports

# ** app
from tiferet.testing import TransferObjectTestBase
from tiferet_mui.domain import Frame
from tiferet_mui.mappers import FrameTransferObject

# *** constants

# ** constant: frame_sample_data
FRAME_SAMPLE_DATA = {
    'elements': [
        {
            'type': 'Stack',
            'props': {'spacing': 2},
            'children': [
                {
                    'type': 'TextField',
                    'props': {'label': 'Name'},
                    'children': [],
                },
            ],
        },
    ],
}

# ** constant: equality_fields
EQUALITY_FIELDS = [
    'elements',
]

# ** constant: element_tree
def ELEMENT_TREE(element):
    '''
    Normalize an element dict or model into a comparable recursive tuple.

    :param element: The element data or domain object.
    :type element: dict | object
    :return: The normalized recursive element tuple.
    :rtype: tuple
    '''

    # Normalize serialized element data.
    if isinstance(element, dict):
        return (
            element['type'],
            element.get('props', {}),
            tuple(ELEMENT_TREE(child) for child in element.get('children', [])),
        )

    # Normalize an Element domain object.
    return (
        element.type,
        element.props,
        tuple(ELEMENT_TREE(child) for child in element.children),
    )

# ** constant: field_normalizers
FIELD_NORMALIZERS = {
    'elements': lambda elements: tuple(ELEMENT_TREE(element) for element in elements),
}

# *** tests

# ** test: TestFrameTransferObject
class TestFrameTransferObject(TransferObjectTestBase):
    '''
    Tests frame mapping and JSON-safe recursive serialization through the harness.
    '''

    # * attribute: transfer_cls
    transfer_cls = FrameTransferObject

    # * attribute: aggregate_cls
    aggregate_cls = Frame

    # * attribute: sample_data
    sample_data = FRAME_SAMPLE_DATA

    # * attribute: aggregate_sample_data
    aggregate_sample_data = FRAME_SAMPLE_DATA

    # * attribute: equality_fields
    equality_fields = EQUALITY_FIELDS

    # * attribute: field_normalizers
    field_normalizers = FIELD_NORMALIZERS

    # * method: test_to_data
    def test_to_data(self):
        '''
        Test the frontend role emits the expected JSON-compatible props tree.
        '''

        # Construct a transfer object from the composed tree data.
        transfer_object = FrameTransferObject.model_validate(FRAME_SAMPLE_DATA)

        # Verify the frontend serialization retains only JSON-compatible tree data.
        assert transfer_object.to_primitive(role='to_data') == FRAME_SAMPLE_DATA
