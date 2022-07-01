from typing import Any

from openpyxl import load_workbook
from openpyxl.worksheet.worksheet import Worksheet


class ExcelParser:

    def parse_excel(self, file: str, sheet_title: str) -> list[dict]:
        """Return list of instance dictionaries from specified excel sheet"""

        wb = load_workbook(filename=file)
        sheet = wb[sheet_title]

        field_names = self._get_fields_names_from_table(sheet)

        items = []
        for row in sheet.iter_rows(min_row=2, values_only=True):
            item = dict()
            for idx in range(len(row)):
                if row[idx] is not None:

                    if field_names[idx] == 'number':
                        value = self._normalize_bill_number(row[idx])
                    elif field_names[idx] == 'sum':
                        value = self._normalize_sum(row[idx])
                    else:
                        value = row[idx]

                    item[field_names[idx]] = value
            if item:
                items.append(item)

        return items

    @staticmethod
    def _get_fields_names_from_table(sheet: Worksheet) -> list[str]:
        """Read first row of table and return list of fileds names for next usage as instance dictionary keys"""

        field_names = []
        for row in sheet.iter_rows(max_row=1, values_only=True):
            for cell in row:

                if cell is not None:
                    if cell == '№':
                        field_names.append('number')
                    else:
                        field_names.append(cell)

        return field_names

    @staticmethod
    def _normalize_bill_number(value: Any) -> int:
        return int(value)

    @staticmethod
    def _normalize_sum(value: Any) -> float:
        return float(value)
