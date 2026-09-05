"""Tiferet MUI Callback Events."""

# *** imports

# ** core
from typing import Any, Callable, Dict, Iterator, Tuple

# ** app
from tiferet.events import DomainEvent

from .. import assets as a
from ..domain import CallbackTable, Element, Frame
from ..mappers import CallbackTableAggregate

# *** events

# ** event: build_callback_table
class BuildCallbackTable(DomainEvent):
    '''
    Turns the callable-bearing elements of one frame into a stable, frozen
    callback registry that the host can safely render and later dispatch.
    '''

    # * method: execute
    @DomainEvent.parameters_required(['frame'])
    def execute(self, frame: Frame, **kwargs) -> CallbackTable:
        '''
        Build a callback table from the frame's interactive element tree.

        Each callable element prop marks an interactive element. The callable
        is registered under a generated identifier and replaced in the prop
        mapping with that identifier, preserving a JSON-safe render payload.

        :param frame: The composed frame whose element tree is registered.
        :type frame: Frame
        :param kwargs: Additional event parameters.
        :type kwargs: dict
        :return: The frozen callback table for the frame.
        :rtype: CallbackTable
        '''

        # Verify the required value is a composed frame before walking it.
        self.verify(
            expression=isinstance(frame, Frame),
            error_code=a.CALLBACK_NOT_FOUND_ID,
            message='A callback table can only be built from a Frame.',
        )

        # Build registrations while assigning identifiers in tree-walk order.
        callback_table = CallbackTableAggregate()
        callback_index = 0
        for element in self._walk(frame.elements):
            handler_prop, handler = self._get_handler(element)
            if handler is None:
                continue

            callback_id = f'callback_{callback_index:02d}'
            callback_table.register(callback_id, handler)
            element.props[handler_prop] = callback_id
            element.props['callback_id'] = callback_id
            callback_index += 1

        # Return the aggregate's immutable domain snapshot.
        return callback_table.freeze()

    # * method: _walk (static)
    @staticmethod
    def _walk(elements: list[Element]) -> Iterator[Element]:
        '''
        Yield every element in depth-first tree-walk order.

        :param elements: The elements at the current tree depth.
        :type elements: list[Element]
        :return: An iterator over each element in the tree.
        :rtype: Iterator[Element]
        '''

        # Yield the current element before recursively yielding its descendants.
        for element in elements:
            yield element
            yield from BuildCallbackTable._walk(element.children)

    # * method: _get_handler (static)
    @staticmethod
    def _get_handler(element: Element) -> Tuple[str | None, Callable[..., Any] | None]:
        '''
        Find the first callable prop that makes an element interactive.

        :param element: The element whose props are inspected.
        :type element: Element
        :return: The handler-prop name and callable, when present.
        :rtype: Tuple[str | None, Callable[..., Any] | None]
        '''

        # Return the first callable property without branching by widget type.
        for prop_name, value in element.props.items():
            if callable(value):
                return prop_name, value

        # Report that the element has no registered interaction.
        return None, None

# ** event: dispatch_callback
class DispatchCallback(DomainEvent):
    '''
    Delivers one reported interaction to the handler registered for its
    callback identifier, making unclaimed interactions explicit domain errors.
    '''

    # * method: execute
    @DomainEvent.parameters_required(['callback_table', 'payload'])
    def execute(
            self,
            callback_table: CallbackTable,
            payload: Dict[str, Any],
            **kwargs,
        ) -> Any:
        '''
        Resolve and invoke the handler for one composite interaction payload.

        :param callback_table: The callback snapshot for the current frame.
        :type callback_table: CallbackTable
        :param payload: The payload containing one callback ID and a timestamp.
        :type payload: Dict[str, Any]
        :param kwargs: Additional event parameters.
        :type kwargs: dict
        :return: The value returned by the registered handler.
        :rtype: Any
        '''

        # Verify the payload uses the confirmed composite mapping shape.
        self.verify(
            expression=isinstance(payload, dict),
            error_code=a.CALLBACK_NOT_FOUND_ID,
            message='A callback payload must be a mapping.',
        )
        self.verify(
            expression='timestamp' in payload,
            error_code=a.CALLBACK_NOT_FOUND_ID,
            message='A callback payload must include a timestamp.',
        )

        # Resolve the single callback entry defined by the confirmed payload shape.
        callback_entries = [
            (callback_id, parameters)
            for callback_id, parameters in payload.items()
            if callback_id != 'timestamp'
        ]
        self.verify(
            expression=len(callback_entries) == 1,
            error_code=a.CALLBACK_NOT_FOUND_ID,
            message='A callback payload must contain exactly one callback_id.',
        )
        callback_id, parameters = callback_entries[0]

        # Resolve the registered handler or report the unclaimed interaction.
        handler = callback_table.handlers.get(callback_id)
        if handler is None:
            self.raise_error(
                a.CALLBACK_NOT_FOUND_ID,
                callback_id=callback_id,
            )

        # Invoke the resolved handler with the callback-defined parameters.
        return handler(**parameters)
