import uuid

class UUIDFormat():

    @classmethod
    def is_valid_uuid(self, value):
        try:
            uuid.UUID(str(value), version=4)
            return True
        except ValueError:
            return False