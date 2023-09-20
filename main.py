from business_logic import ContractService, ProjectService
from business_logic.errors import (ActiveContractsAlreadyExistError,
                                   ContractDoesNotExistError,
                                   ContractHasUsedWithAtherProjectError,
                                   InvalidContractStatusError,
                                   NoContractsError, ProjectAlreadyExistsError,
                                   ProjectDoesNotExistError)
from presentation_layer.config import DB_NAME, DB_TYPE
from presentation_layer.db_provider import db_provider
from presentation_layer.errors import (InvalidChoiceNumberError,
                                       InvalidChoiceTypeError,
                                       InvalidDBTypeError,
                                       InvalidNumberTypeError)
from presentation_layer.validators import (validate_choice,
                                           validate_contract_number)

while True:
    choice = input(
        "1 - Project\n"
        "2 - Contract\n"
        "3 - Contract list\n"
        "4 - Project list\n"
        "5 - Exit\n"
        "Your choice: "
    )

    try:
        validate_choice(choice=choice, start=1, stop=5)
    except InvalidChoiceNumberError as err:
        print(err)
        continue
    except InvalidChoiceTypeError as err:
        print(err)
        continue

    try:
        connector = db_provider(db_name=DB_NAME, db_type=DB_TYPE)
    except InvalidDBTypeError as err:
        print(err)
        continue

    if int(choice) == 1:
        inner_choice = input(
            "1 - Create a project\n"
            "2 - Add a contract\n"
            "3 - Complete a contract\n"
            "4 - Project list\n"
            "5 - Back to previous menu\n"
            "Your choice: "
        )
        try:
            validate_choice(choice=inner_choice, start=1, stop=5)
        except InvalidChoiceNumberError as err:
            print(err)
            continue
        except InvalidChoiceTypeError as err:
            print(err)
            continue

        if int(inner_choice) == 1:
            try:
                name = input("Enter a project name: ").lower()
                ProjectService(db_connector=connector).create_project(name=name)
                print(f"The project '{name.capitalize()}' has been created.")
            except ProjectAlreadyExistsError as err:
                print(err)
                continue
            except NoContractsError as err:
                print(err)
                continue

        elif int(inner_choice) == 2:
            project_name = input("Enter a project name: ").lower()
            try:
                project_id = ProjectService(db_connector=connector).get_id_by_name(
                    name=project_name
                )
            except ProjectDoesNotExistError as err:
                print(err)
                continue

            contract_id = input("Enter a number of contract: ")
            try:
                validate_contract_number(data=contract_id)
            except InvalidNumberTypeError as err:
                print(err)
                continue

            try:
                ContractService(db_connector=connector).add_project(
                    project_id=project_id, contract_id=int(contract_id)
                )
            except ContractHasUsedWithAtherProjectError as err:
                print(err)
                continue
            except InvalidContractStatusError as err:
                print(err)
                continue
            except ActiveContractsAlreadyExistError as err:
                print(err)
                continue
            except ContractDoesNotExistError as err:
                print(err)
                continue

            print(
                f"The contract '{contract_id}'"
                f" has been added to the project {project_name.capitalize()}."
            )

        elif int(inner_choice) == 3:
            contract_id = input("Enter a number of contract: ")
            try:
                validate_contract_number(data=contract_id)
            except InvalidNumberTypeError as err:
                print(err)
                continue

            ContractService(db_connector=connector).complete_contract(
                contract_id=int(contract_id)
            )
            print(f"The contract '{contract_id}' has been completed.")

        elif int(inner_choice) == 4:
            projects = ProjectService(db_connector=connector).get_all_projects()
            for project in projects:
                print(
                    f"Project id: {project.project_id}\n"
                    f"Project name: {project.name}\n"
                    f"Created at: {project.created_at}\n"
                    f"Contracts:"
                )
                for contract in project.contracts:
                    print(
                        f"    Contract id: {contract[0]}\n"
                        f"    Contract name: {contract[1]}\n"
                        f"    Contract status: {contract[2]}\n"
                    )

        elif int(inner_choice) == 5:
            continue

    elif int(choice) == 2:
        inner_choice = input(
            "1 - Create a contract\n"
            "2 - Confirm a contract\n"
            "3 - Complete a contract\n"
            "4 - Contract list\n"
            "5 - Back to previous menu\n"
            "Your choice: "
        )

        try:
            validate_choice(choice=inner_choice, start=1, stop=4)
        except InvalidChoiceNumberError as err:
            print(err)
            continue
        except InvalidChoiceTypeError as err:
            print(err)
            continue

        if int(inner_choice) == 1:
            name = input("Enter a contract name: ").lower()
            ContractService(db_connector=connector).create_contract(name=name)
            print(f"The contract '{name.capitalize()}' has been created.")

        elif int(inner_choice) == 2:
            contract_id = input("Enter a number of contract: ")
            try:
                validate_contract_number(data=contract_id)
            except InvalidNumberTypeError as err:
                print(err)
                continue

            ContractService(db_connector=connector).confirm_contract(
                contract_id=int(contract_id)
            )
            print(f"The contract '{contract_id}' has been confirmed.")

        elif int(inner_choice) == 3:
            contract_id = input("Enter a number of contract: ")
            try:
                validate_contract_number(data=contract_id)
            except InvalidNumberTypeError as err:
                print(err)
                continue

            ContractService(db_connector=connector).complete_contract(
                contract_id=int(contract_id)
            )
            print(f"The contract '{contract_id}' has been completed.")

        elif int(inner_choice) == 4:
            contracts = ContractService(db_connector=connector).get_contracts_list()
            for item in contracts:
                print(
                    f"Contract id: {item.contract_id}\n"
                    f"Contract name: {item.name}\n"
                    f"Contract status: {item.status}\n"
                    f"Signed at: {item.signed_at}\n"
                    f"Project name: {item.project_name}\n"
                    f"Created at: {item.created_at}\n"
                )

        elif int(inner_choice) == 5:
            continue

    elif int(choice) == 3:
        contracts = ContractService(db_connector=connector).get_contracts_list()
        for item in contracts:
            print(
                f"Contract id: {item.contract_id}\n"
                f"Contract name: {item.name}\n"
                f"Contract status: {item.status}\n"
                f"Signed at: {item.signed_at}\n"
                f"Project name: {item.project_name}\n"
                f"Created at: {item.created_at}\n"
            )

    elif int(choice) == 4:
        projects = ProjectService(db_connector=connector).get_all_projects()
        for project in projects:
            print(
                f"Project id: {project.project_id}\n"
                f"Project name: {project.name}\n"
                f"Created at: {project.created_at}\n"
                f"Contracts:"
            )
            for contract in project.contracts:
                print(
                    f"    Contract id: {contract[0]}\n"
                    f"    Contract name: {contract[1]}\n"
                    f"    Contract status: {contract[2]}\n"
                )

    elif int(choice) == 5:
        break
