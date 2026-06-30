"""Protocols for Django site interface."""

from typing import Any, Protocol, TypeVar

T_contra = TypeVar('T_contra', contravariant=True)
T_cov = TypeVar('T_cov', covariant=True)

RequestParams_contra = TypeVar('RequestParams_contra', contravariant=True)
RequestContext_cov = TypeVar('RequestContext_cov', covariant=True)
RequestContext_contra = TypeVar('RequestContext_contra', contravariant=True)
RequestData_cov = TypeVar('RequestData_cov', covariant=True)
RequestData_contra = TypeVar('RequestData_contra', contravariant=True)

Validated_cov = TypeVar('Validated_cov', covariant=True)
Validated_contra = TypeVar('Validated_contra', contravariant=True)
Command_cov = TypeVar('Command_cov', covariant=True)
Command_contra = TypeVar('Command_contra', contravariant=True)
Result_cov = TypeVar('Result_cov', covariant=True)
Result_contra = TypeVar('Result_contra', contravariant=True)

Adapted_cov = TypeVar('Adapted_cov', covariant=True)


###################################################
# DTO components
###################################################


# NOTE: Subject to future null object method additions
class NullProto(Protocol):
    """Protocol for null object."""


class HasHtml(Protocol):
    @property
    def html(self) -> str: ...


class HasContext(Protocol[T_cov]):
    @property
    def context(self) -> T_cov: ...


class HasSessionIdentifier(Protocol):
    @property
    def session_id(self) -> str: ...


class HasData(Protocol[T_cov]):
    @property
    def data(self) -> T_cov: ...


class HasQuery(Protocol[T_cov]):
    @property
    def query(self) -> T_cov: ...


class HtmlResponsible(
    HasHtml,
    HasContext[dict[str, Any]],
    Protocol,
): ...


###################################################
# DTO compositions
###################################################


class SimpleRequestParamsProto(
    HasQuery[NullProto],
    HasContext[RequestContext_cov],
    HasData[RequestData_cov],
): ...


###################################################
# Request handling
###################################################


class Validatable(
    Protocol[
        RequestData_contra,
        Validated_cov,
    ]
):
    def validate(self, data: RequestData_contra) -> Validated_cov: ...


class Preparable(
    Protocol[
        RequestParams_contra,
        RequestContext_contra,
        Validated_contra,
        Command_cov,
    ]
):
    def prepare(
        self,
        params: RequestParams_contra,
        context: RequestContext_contra,
        data: Validated_contra,
    ) -> Command_cov: ...


class ResponseAdaptable(
    Protocol[Result_contra, RequestData_contra, Adapted_cov],
):
    def to_response(
        self,
        source: Result_contra,
        context: RequestData_contra,
    ) -> Adapted_cov: ...
