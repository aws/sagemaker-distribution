from __future__ import absolute_import


class RequirementsInstallException(Exception):
    pass


class InferenceCodeLoadException(Exception):
    pass


class ServerStartException(Exception):
    pass


class SyncInvocationsException(Exception):
    pass


class AsyncInvocationsException(Exception):
    pass
