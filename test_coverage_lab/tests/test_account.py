"""
Test Cases for Account Model
"""

import json
from random import randrange
import pytest
from models import db
from models.account import Account, DataValidationError

ACCOUNT_DATA = {}

@pytest.fixture(scope="module", autouse=True)
def load_account_data():
    """Load data needed by tests"""
    global ACCOUNT_DATA
    with open("tests/fixtures/account_data.json") as json_data:
        ACCOUNT_DATA = json.load(json_data)

    # Set up the database tables
    db.create_all()
    yield
    db.session.close()


@pytest.fixture
def setup_account():
    """Fixture to create a test account"""
    account = Account(name="John businge", email="john.businge@example.com")
    db.session.add(account)
    db.session.commit()
    return account

@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown():
    """ Truncate the tables and set up for each test """

@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown():
    """Truncate the tables and set up for each test"""
    db.session.query(Account).delete()
    db.session.commit()
    yield
    db.session.remove()


######################################################################
#  E X A M P L E   T E S T   C A S E
######################################################################

# ===========================
# Test Group: Role Management
# ===========================

# ===========================
# Test: Account Role Assignment
# Author: John Businge
# Date: 2025-01-30
# Description: Ensure roles can be assigned and checked.
# ===========================


def test_account_role_assignment():
    """Test assigning roles to an account"""
    account = Account(name="John Doe", email="johndoe@example.com", role="user")

    # Assign initial role
    assert account.role == "user"

    # Change role and verify
    account.change_role("admin")
    assert account.role == "admin"


# ===========================
# Test: Invalid Role Assignment
# Author: John Businge
# Date: 2025-01-30
# Description: Ensure invalid roles raise a DataValidationError.
# ===========================


def test_invalid_role_assignment():
    """Test assigning an invalid role"""
    account = Account(role="user")

    # Attempt to assign an invalid role
    with pytest.raises(DataValidationError):
        account.change_role("moderator")  # Invalid role should raise an error


######################################################################
#  T O D O   T E S T S  (To Be Completed by Students)
######################################################################

"""
Each student in the team should implement **one test case** from the list below.
The team should coordinate to **avoid duplicate work**.

Each test should include:
- A descriptive **docstring** explaining what is being tested.
- **Assertions** to verify expected behavior.
- A meaningful **commit message** when submitting their PR.
"""

# Test Assignments

# Student 1: Test account serialization
# - Verify that the account object is correctly serialized to a dictionary.
# - Ensure all expected fields are included in the output.
# Target Method: to_dict()

# Student 2: Test invalid email input
# - Ensure invalid email formats raise a validation error.
# Target Method: validate_email()
# ===========================
# Test: Account Serialization
# Author: Daniel Mamuza
# Date: 2026-02-09
# Description: Ensure Account.to_dict() returns a correct dictionary representation.
# ===========================
def test_account_serialization():
    """Test that an account serializes to a dictionary"""
    account = Account(
        name="Thorfinn",
        email="no.enemies@vinland.com",
        phone_number="123456789",
        disabled=False,
        balance=0.0,
        role="user",
    )

    db.session.add(account)
    db.session.commit()

    data = account.to_dict()

    # verify type and serialized values
    assert isinstance(data, dict)
    assert "password_hash" not in data
    assert data == {
        "id": account.id,
        "name": "Thorfinn",
        "email": "no.enemies@vinland.com",
        "phone_number": "123456789",
        "disabled": False,
        "date_joined": account.date_joined,
        "balance": 0.0,
        "role": "user",
    }

# ===========================
# Test: Invalid Email Handling
# Author: Hristiyan Melios
# Date: 2026-02-16
# Description: - Ensure invalid emails raise a DataValidationError.
# Ensure accounts without an email cannot be created.
# ===========================
def test_invalid_email_handling():

    # Attempt to assign no email.
    account = Account(role="user")
    with pytest.raises(TypeError): # match() can't accept None type.
        account.validate_email()

    # Attempt invalid email: No '@' symbol.
    account = Account(role="user", email="not-an-email")
    with pytest.raises(DataValidationError):
        account.validate_email()

    # Attempt invalid email: No '.' symbol after '@'.
    account = Account(role="user", email="not-an-email@gmail")
    with pytest.raises(DataValidationError):
        account.validate_email()

    # Attempt invalid email: No text after '.'
    account = Account(role="user", email="not-an-email@gmail.")
    with pytest.raises(DataValidationError):
        account.validate_email()

    # Attempt invalid email: No text before after '@'.
    account = Account(role="user", email="@gmail.com")
    with pytest.raises(DataValidationError):
        account.validate_email()

    # Attempt invalid email: Special characters.
    account = Account(role="user", email="gorilla-sushi@gmail.com!")
    with pytest.raises(DataValidationError):
        account.validate_email()

# Student 3: Test missing required fields
# - Ensure account initialization fails when required fields are missing.
# Target Method: Account() initialization

# Student 4: Test positive deposit
# - Verify that depositing a positive amount correctly increases the balance.
# Target Method: deposit()
# ===========================
# Test: Test Positive Deposit
# Author: Reece Galgana
# Date: 2025-02-11
# Description: Verify that depositing a positive amount correctly increases the balance.
# ===========================
def test_positive_deposit():

    account = Account(name="Gorilla Sushi", email="gorillasushi@gmail.com", role="user", balance = 0)

    # Depositing small positive integer increases balance accordingly.
    account.deposit(1)
    assert account.balance == 1

    # Depositing large positive integer increases balance accordingly.
    account.deposit(2**32)
    assert account.balance == (2**32) + 1

    # Depositing small positive float increases balance accordingly.
    account.deposit(1.982)
    assert account.balance == (2**32) + 1 + 1.982

    # Depositing small positive float increases balance accordingly.
    account.deposit(2**32.1)
    assert account.balance == (2**32) + 1 + 1.982 + (2**32.1)


# Student 5: Test deposit with zero/negative values
# - Ensure zero or negative deposits are rejected.
# Target Method: deposit()

# Student 6: Test valid withdrawal
# - Verify that withdrawing a valid amount correctly decreases the balance.
# Target Method: withdraw()

# Student 7: Test withdrawal with insufficient funds
# - Ensure withdrawal fails when balance is insufficient.
# Target Method: withdraw()
# ===========================
# Test: Test Withdrawl With Insufficient Funds
# Author: Jonah Lewis
# Date: 2025-02-15
# Description: Verify that withdrawing an amount larger than the account balance raises an exception
# ===========================
def test_withdrawl_insufficient_funds():
    """Test withdrawing from an account with insufficient funds"""

    account = Account(balance=0)
    with pytest.raises(DataValidationError):
        account.withdraw(1)

# Student 8: Test password hashing
# - Ensure passwords are properly hashed.
# - Verify that password verification works correctly.
# Target Methods: set_password() / check_password()

# ===========================
# Test: Password Hashing
# Author: Nathan Dela Pena
# Date: 2026-02-16
# Description: Test password hashing
# ===========================

def test_password_hashing(setup_account):
    account = setup_account

    # set a password
    account.set_password("Testing123!")

    # ensure the password is not stored as a string
    assert account.password_hash != "Testing123!"
    assert account.password_hash is not None

    # verify the password
    assert account.check_password("Testing123!") is True

    # testing wrong password
    assert account.check_password("Wrongpas!") is False


# Student 9: Test account deactivation/reactivation
# - Ensure accounts can be deactivated and reactivated correctly.
# Target Methods: deactivate() / reactivate()
# ===========================
# Test: Account Deactivation and Reactivation
# Author: Jessey Morales Trejo
# Date: 2026-02-16
# Description: Ensure accounts can be deactivated and reactivated correctly.
# ===========================

def test_account_deactivation_reactivation():
#Test that an account can be deactivated and reactivated

    account = Account(name="Test User", email="testuser@example.com")
    db.session.add(account)
    db.session.commit()

    assert account.disabled is False

    account.deactivate()
    db.session.commit()

    retrieved = Account.query.filter_by(email="testuser@example.com").first()
    assert retrieved.disabled is True

    retrieved.reactivate()
    db.session.commit()

    updated = Account.query.filter_by(email="testuser@example.com").first()
    assert updated.disabled is False

# Student 10: Test email uniqueness enforcement
# - Ensure duplicate emails are not allowed.
# Target Method: validate_unique_email()

# Student 11: Test deleting an account
# - Verify that an account can be successfully deleted from the database.
# Target Method: delete()
# Target Method: delete()
