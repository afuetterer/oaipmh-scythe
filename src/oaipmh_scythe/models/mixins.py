# SPDX-FileCopyrightText: 2024 Heinz-Alexander Fütterer
#
# SPDX-License-Identifier: BSD-3-Clause

"""TODO."""

from typing import Any


class HeaderMixin:
    """A mixin class that provides functionality for managing headers in records.

    Attributes:
        status: The status attribute of the header.
    """

    status: Any

    @property
    def deleted(self) -> bool:
        """Indicate if this header has been deleted.

        Returns:
            True if the status attribute contains DELETED, False otherwise.
        """
        if self.status and self.status.DELETED:
            return True
        return False


class RecordMixin:
    """A mixin class that provides functionality for managing records.

    Attributes:
        header: The header of the record.
        metadata: The metadata associated with the record.
    """

    header: Any
    metadata: Any

    @property
    def deleted(self) -> bool:
        """Indicate if this record has been deleted.

        Returns:
            True if the header's status attribute contains DELETED, False otherwise.
        """
        if self.header.status and self.header.status.DELETED:
            return True
        return False

    def get_metadata(self):
        """Return the metadata associated with this record.

        Returns:
            The metadata associated with this record.
        """
        return self.metadata.other_element
