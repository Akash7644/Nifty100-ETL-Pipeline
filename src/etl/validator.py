import pandas as pd


class ValidationError:
    def __init__(self, rule, severity, table, row, message):
        self.rule = rule
        self.severity = severity
        self.table = table
        self.row = row
        self.message = message

    def to_dict(self):
        return {
            "Rule": self.rule,
            "Severity": self.severity,
            "Table": self.table,
            "Row": self.row,
            "Message": self.message
        }


class Validator:
    def __init__(self):
        self.errors = []

    def add_error(self, rule, severity, table, row, message):
        self.errors.append(
            ValidationError(
                rule,
                severity,
                table,
                row,
                message
            )
        )

    def export_failures(self, output_path):
        df = pd.DataFrame(
            [error.to_dict() for error in self.errors]
        )
        df.to_csv(output_path, index=False)

    def summary(self):
        print("=" * 40)
        print("Validation Summary")
        print("=" * 40)
        print(f"Total Issues : {len(self.errors)}")

        critical = sum(
            error.severity == "CRITICAL"
            for error in self.errors
        )

        warning = sum(
            error.severity == "WARNING"
            for error in self.errors
        )

        print(f"Critical : {critical}")
        print(f"Warning  : {warning}")