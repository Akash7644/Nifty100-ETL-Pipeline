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
            ValidationError(rule, severity, table, row, message)
        )

    # -------------------------
    # DQ-01 Primary Key Uniqueness
    # -------------------------
    def check_primary_key_uniqueness(self, df, primary_key, table_name):
        duplicates = df[df.duplicated(subset=[primary_key], keep=False)]

        if duplicates.empty:
            return

        for index, row in duplicates.iterrows():
            self.add_error(
                rule="DQ-01",
                severity="CRITICAL",
                table=table_name,
                row=index + 2,
                message=f"Duplicate {primary_key}: {row[primary_key]}"
            )

    # -------------------------
    # DQ-02 Composite Key
    # -------------------------
    def check_composite_key_uniqueness(self, df, columns, table_name):
        duplicates = df[df.duplicated(subset=columns, keep=False)]

        if duplicates.empty:
            return

        for index, row in duplicates.iterrows():
            values = ", ".join(str(row[col]) for col in columns)

            self.add_error(
                rule="DQ-02",
                severity="CRITICAL",
                table=table_name,
                row=index + 2,
                message=f"Duplicate ({', '.join(columns)}): {values}"
            )

    # -------------------------
    # DQ-03 Foreign Key
    # -------------------------
    def check_foreign_key(self, child_df, parent_df, child_key, parent_key, table_name):
        invalid = child_df[
            ~child_df[child_key].isin(parent_df[parent_key])
        ]

        if invalid.empty:
            return

        for index, row in invalid.iterrows():
            self.add_error(
                rule="DQ-03",
                severity="CRITICAL",
                table=table_name,
                row=index + 2,
                message=f"{child_key} '{row[child_key]}' not found in parent table"
            )

    # -------------------------
    # DQ-04 to DQ-16
    # -------------------------
    def check_balance_sheet(self, df, table_name="balancesheet"):
        invalid = df[
            (df["total_assets"] - df["total_liabilities"]).abs() > 1
        ]

        for index, row in invalid.iterrows():
            self.add_error(
                rule="DQ-04",
                severity="CRITICAL",
                table=table_name,
                row=index + 2,
                message=(
                    f"Balance Sheet mismatch: "
                    f"Assets={row['total_assets']}, "
                    f"Liabilities={row['total_liabilities']}"
                )
            )  

    def check_operating_margin(self, df, table_name="profitandloss"):
        valid = df[df["sales"] != 0]

        calculated = (
            valid["operating_profit"] /
            valid["sales"]
        ) * 100

        invalid = valid[
            (calculated - valid["opm_percentage"]).abs() > 1
        ]

        for index, row in invalid.iterrows():
            self.add_error(
                rule="DQ-05",
                severity="WARNING",
                table=table_name,
                row=index + 2,
                message="Operating Margin percentage is inconsistent."
            )

    def check_positive_sales(self, df, table_name="profitandloss"):
        invalid = df[df["sales"] < 0]

        for index, row in invalid.iterrows():
            self.add_error(
                rule="DQ-06",
                severity="CRITICAL",
                table=table_name,
                row=index + 2,
                message=f"Negative Sales: {row['sales']}"
            )

    def check_net_cash(self, df, table_name="cashflow"):
        calculated = (
            df["operating_activity"] +
            df["investing_activity"] +
            df["financing_activity"]
        )

        invalid = df[
            (calculated - df["net_cash_flow"]).abs() > 1
        ]

        for index, row in invalid.iterrows():
            self.add_error(
                rule="DQ-07",
                severity="WARNING",
                table=table_name,
                row=index + 2,
                message="Net Cash Flow calculation mismatch."
            )

    def check_tax_rate(self, df, table_name="profitandloss"):
        invalid = df[
            (df["tax_percentage"] < 0) |
            (df["tax_percentage"] > 100)
        ]

        for index, row in invalid.iterrows():
            self.add_error(
                rule="DQ-08",
                severity="WARNING",
                table=table_name,
                row=index + 2,
                message=f"Invalid Tax Percentage: {row['tax_percentage']}"
            )

    def check_dividend_cap(self, df, table_name="profitandloss"):
        invalid = df[
            (df["dividend_payout"] < 0) |
            (df["dividend_payout"] > 100)
        ]

        for index, row in invalid.iterrows():
            self.add_error(
                rule="DQ-09",
                severity="WARNING",
                table=table_name,
                row=index + 2,
                message=f"Invalid Dividend Payout: {row['dividend_payout']}"
            )

    def check_url(self, df, table_name="companies"):
        invalid = df[
            ~df["website"].fillna("").str.match(
                r"^https?://",
                case=False
            )
        ]

        for index, row in invalid.iterrows():
            self.add_error(
                rule="DQ-10",
                severity="WARNING",
                table=table_name,
                row=index + 2,
                message=f"Invalid Website URL: {row['website']}"
            )

    def check_eps_sign(self, df, table_name="profitandloss"):
        invalid = df[
            (
                (df["net_profit"] > 0) &
                (df["eps"] < 0)
            ) |
            (
                (df["net_profit"] < 0) &
                (df["eps"] > 0)
            )
        ]

        for index, row in invalid.iterrows():
            self.add_error(
                rule="DQ-11",
                severity="WARNING",
                table=table_name,
                row=index + 2,
                message="EPS sign is inconsistent with Net Profit."
            )

    def check_id_uniqueness(self, df, table_name):
        duplicates = df[df.duplicated(subset=["id"], keep=False)]

        for index, row in duplicates.iterrows():
            self.add_error(
                rule="DQ-16",
                severity="CRITICAL",
                table=table_name,
                row=index + 2,
                message=f"Duplicate ID: {row['id']}"
            )

    def check_year_coverage(self, df, table_name):
        invalid = df[
            (df["year"] < 2000) |
            (df["year"] > 2035)
        ]

        for index, row in invalid.iterrows():
            self.add_error(
                rule="DQ-12",
                severity="WARNING",
                table=table_name,
                row=index + 2,
                message=f"Invalid Year: {row['year']}"
            )

    def check_missing_values(self, df, mandatory_columns, table_name):
        for column in mandatory_columns:
            missing = df[df[column].isnull()]

            for index, row in missing.iterrows():
                self.add_error(
                    rule="DQ-13",
                    severity="CRITICAL",
                    table=table_name,
                    row=index + 2,
                    message=f"Missing value in '{column}'"
                )

    def check_negative_values(self, df, columns, table_name):
        for column in columns:
            invalid = df[df[column] < 0]

            for index, row in invalid.iterrows():
                self.add_error(
                    rule="DQ-14",
                    severity="CRITICAL",
                    table=table_name,
                    row=index + 2,
                    message=f"Negative value in '{column}': {row[column]}"
                )
                
    def check_duplicate_rows(self, df, table_name):
        duplicates = df[df.duplicated(keep=False)]

        for index, row in duplicates.iterrows():
            self.add_error(
                rule="DQ-15",
                severity="WARNING",
                table=table_name,
                row=index + 2,
                message="Duplicate row found."
            )

    def export_failures(self, output_path):
        df = pd.DataFrame([error.to_dict() for error in self.errors])
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
