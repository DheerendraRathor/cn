from typing import List, Mapping
from typing import Tuple


class VerificationChoices(object):
    PENDING = 0
    VERIFIED = 1
    REJECTED = 2

    @classmethod
    def choices(cls) -> List[Tuple[int, str]]:
        return [
            (cls.PENDING, 'Pending'),
            (cls.VERIFIED, 'Verified'),
            (cls.REJECTED, 'Rejected'),
        ]

    @classmethod
    def validation_choices(cls) -> List[Tuple[int, str]]:
        return [
            (cls.VERIFIED, 'Verified'),
            (cls.REJECTED, 'Rejected'),
        ]

    @classmethod
    def to_dict(cls) -> Mapping[int, str]:
        return {
            cls.PENDING: 'Pending',
            cls.VERIFIED: 'Verified',
            cls.REJECTED: 'Rejected',
        }

    @staticmethod
    def get_glyphicon_html(verification_type: 'VerificationChoices') -> str:
        if verification_type == VerificationChoices.VERIFIED:
            return """
            <span class="text-success" title="Verified">
                <span class="glyphicon glyphicon-ok-sign"></span>
            </span>
            """

        if verification_type == VerificationChoices.REJECTED:
            return """
            <span class="text-danger" title="Rejected">
                <span class="glyphicon glyphicon-remove-sign"></span>
            </span>
            """

        if verification_type == VerificationChoices.PENDING:
            return """
            <span class="text-warning" title="Pending">
                <span class="glyphicon glyphicon-remove-sign"></span>
            </span>
            """


class OrganizationObjectType(object):
    POST = 0
    AWARD = 1

    @classmethod
    def to_dict(cls) -> Mapping[int, str]:
        return {
            cls.POST: 'Post',
            cls.AWARD: 'Award',
        }

    @classmethod
    def choices(cls) -> List[Tuple[int, str]]:
        return [(k, v) for k, v in cls.to_dict().items()]


MAX_RECIPIENTS = 100000
