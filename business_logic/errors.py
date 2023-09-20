class NoContractsError(Exception):
    ...


class ProjectDoesNotExistError(Exception):
    ...


class ProjectAlreadyExistsError(Exception):
    ...


class ContractDoesNotExistError(Exception):
    ...


class InvalidContractStatusError(Exception):
    ...


class ActiveContractsAlreadyExistError(Exception):
    ...


class ContractHasUsedWithAtherProjectError(Exception):
    ...
