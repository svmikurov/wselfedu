"""Protocols for request handler interface."""

from __future__ import annotations

from typing import Protocol, TypeVar

Params_contra = TypeVar('Params_contra', contravariant=True)
Context_contra = TypeVar('Context_contra', contravariant=True)
Data_contra = TypeVar('Data_contra', contravariant=True)
Result_cov = TypeVar('Result_cov', covariant=True)


class RequestHandlerProtocol(
    Protocol[Params_contra, Context_contra, Data_contra, Result_cov]
):
    """Protocol for request handler."""

    def execute(
        self,
        params: Params_contra,
        context: Context_contra,
        data: Data_contra,
    ) -> Result_cov:
        """Execute."""
