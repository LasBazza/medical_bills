from openpyxl import load_workbook


class ExcelParser:

    def parse_excel(self, file, sheet_title):
        wb = load_workbook(filename=file, read_only=True)
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
    def _get_fields_names_from_table(sheet):

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
    def _normalize_bill_number(value):
        return int(value)

    @staticmethod
    def _normalize_sum(value):
        return float(value)
