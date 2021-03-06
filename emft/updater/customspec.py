# coding=utf-8
import typing

from semantic_version import Spec as SemanticSpec

from emft.core.logging import make_logger
from . import channel
from .customversion import CustomVersion

LOGGER = make_logger(__name__)


class CustomSpec(SemanticSpec):
    def __init__(self, *spec_strings):
        SemanticSpec.__init__(self, *spec_strings)

    def filter_channel(
        self,
        versions: typing.Set[CustomVersion],
        prerelease: str = channel.STABLE
    ):
        LOGGER.debug(f'filtering {len(versions)} versions against {self}')
        unknown_pre_release_tags = set()
        for version in super(CustomSpec, self).filter(versions):
            assert isinstance(version, CustomVersion)
            if version.prerelease:
                if not prerelease:
                    if 'prerelease' not in unknown_pre_release_tags:
                        unknown_pre_release_tags.add('prerelease')
                        LOGGER.debug(f'skipping pre-release "{version}"')
                    continue
                if version.prerelease[0] in ('PullRequest',):
                    if 'pull request' not in unknown_pre_release_tags:
                        unknown_pre_release_tags.add('pull request')
                        LOGGER.debug(f'skipping pull-request "{version}"')
                    continue
                if version.prerelease[0] not in channel.PRE_RELEASE_LABELS:
                    if version.prerelease[0] not in unknown_pre_release_tags:
                        unknown_pre_release_tags.add(version.prerelease[0])
                        LOGGER.debug(f'skipping unknown pre-release tag "{version.prerelease[0]}"')
                    continue
                if version.prerelease[0] < prerelease:
                    LOGGER.debug(f'skipping pre-release "{version}" because it is not on channel "{prerelease}"')
                    continue
            yield version

    def select_channel(
        self,
        versions: typing.Set[CustomVersion],
        update_channel: str = channel.STABLE
    ) -> typing.Union[CustomVersion, None]:
        """
        Selects the latest version, equals or higher than "channel"

        Args:
            versions: versions to select from
            update_channel: member of :class:`Channel`

        Returns: latest version or None

        """
        LOGGER.debug(f'selecting latest version amongst {len(versions)}; active channel: {str(channel)}')
        options = list(self.filter_channel(versions, update_channel))
        if options:
            latest = max(options)
            return latest
        LOGGER.debug('no version passed the test')
        return None
