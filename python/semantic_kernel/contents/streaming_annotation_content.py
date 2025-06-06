# Copyright (c) Microsoft. All rights reserved.

import logging
from typing import Any, ClassVar, Literal, TypeVar
from xml.etree.ElementTree import Element  # nosec

from pydantic import Field

from semantic_kernel.contents.const import STREAMING_ANNOTATION_CONTENT_TAG, ContentTypes
from semantic_kernel.contents.kernel_content import KernelContent
from semantic_kernel.utils.feature_stage_decorator import experimental

logger = logging.getLogger(__name__)

_T = TypeVar("_T", bound="StreamingAnnotationContent")


@experimental
class StreamingAnnotationContent(KernelContent):
    """Streaming Annotation content."""

    content_type: Literal[ContentTypes.STREAMING_ANNOTATION_CONTENT] = Field(
        STREAMING_ANNOTATION_CONTENT_TAG,  # type: ignore
        init=False,
    )
    tag: ClassVar[str] = STREAMING_ANNOTATION_CONTENT_TAG
    file_id: str | None = None
    quote: str | None = None
    start_index: int | None = None
    end_index: int | None = None
    url: str | None = None

    def __str__(self) -> str:
        """Return the string representation of the annotation content."""
        return f"StreamingAnnotationContent(file_id={self.file_id}, url={self.url}, quote={self.quote}, start_index={self.start_index}, end_index={self.end_index})"  # noqa: E501

    def to_element(self) -> Element:
        """Convert the annotation content to an Element."""
        element = Element(self.tag)
        if self.file_id:
            element.set("file_id", self.file_id)
        if self.quote:
            element.set("quote", self.quote)
        if self.start_index is not None:
            element.set("start_index", str(self.start_index))
        if self.end_index is not None:
            element.set("end_index", str(self.end_index))
        if self.url is not None:
            element.set("url", self.url)
        return element

    @classmethod
    def from_element(cls: type[_T], element: Element) -> _T:
        """Create an instance from an Element."""
        return cls(
            file_id=element.get("file_id"),
            quote=element.get("quote"),
            start_index=int(element.get("start_index")) if element.get("start_index") else None,  # type: ignore
            end_index=int(element.get("end_index")) if element.get("end_index") else None,  # type: ignore
            url=element.get("url") if element.get("url") else None,  # type: ignore
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert the instance to a dictionary."""
        return {
            "type": "text",
            "text": f"{self.file_id or self.url} {self.quote} (Start Index={self.start_index}->End Index={self.end_index})",  # noqa: E501
        }
