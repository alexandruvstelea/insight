from sqlalchemy.exc import IntegrityError


class ErrorFormatter:

    @staticmethod
    def format_integrity_error(e: IntegrityError) -> dict:
        if "unique constraint" in str(e.orig):
            return {"code": 409, "detail": "An item with this name already exists."}
        elif "foreign key constraint" in str(e.orig):
            return {"code": 404, "detail": "Referenced entity does not exist."}
        else:
            return {"code": 400, "detail": f"An integrity error occurred."}
