"""Builder type aliases."""

from typing import TypeVar

LockupCommand = TypeVar('LockupCommand')
LockupConditions = TypeVar('LockupConditions')

SpecT = TypeVar('SpecT')
Spec_contra = TypeVar('Spec_contra', contravariant=True)
CandidateT = TypeVar('CandidateT')
Candidate_contra = TypeVar('Candidate_contra', contravariant=True)

DTO = TypeVar('DTO')
DTO_contra = TypeVar('DTO_contra', contravariant=True)
DTO_co = TypeVar('DTO_co', covariant=True)

DomainT_contra = TypeVar('DomainT_contra', contravariant=True)
DtoT = TypeVar('DtoT')
Result_co = TypeVar('Result_co', covariant=True)
