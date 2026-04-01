class AppError(Exception):
    pass


class NotFoundError(AppError):
    def __init__(self, entity: str, entity_id=None):
        self.detail = f"{entity} not found" + (f": {entity_id}" if entity_id else "")
        super().__init__(self.detail)


class UserNotFoundError(NotFoundError):
    def __init__(self, entity_id=None):
        super().__init__("User", entity_id)


class ContactNotFoundError(NotFoundError):
    def __init__(self, entity_id=None):
        super().__init__("Contact", entity_id)


class ExpenseNotFoundError(NotFoundError):
    def __init__(self, entity_id=None):
        super().__init__("Expense", entity_id)


class ExpenseSplitNotFoundError(NotFoundError):
    def __init__(self, entity_id=None):
        super().__init__("Expense split", entity_id)


class PaymentNotFoundError(NotFoundError):
    def __init__(self, entity_id=None):
        super().__init__("Payment", entity_id)


class ChatNotFoundError(NotFoundError):
    def __init__(self, entity_id=None):
        super().__init__("Chat", entity_id)


class MessageNotFoundError(NotFoundError):
    def __init__(self, entity_id=None):
        super().__init__("Message", entity_id)
