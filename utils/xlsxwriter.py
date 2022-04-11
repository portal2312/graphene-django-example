"""xlsxwriter base."""
import io
from collections import defaultdict
from enum import Enum

import xlsxwriter


__all__ = ["ExcelError", "Excel", "MIMETypeEnum"]


class ExcelError(Exception):
    """Excel error exception."""


class Excel:
    """Creating excel file with xlsxwriter.

    References:
        https://xlsxwriter.readthedocs.io/
    """

    def __init__(self, filename=None, **options):
        """Init.

        Args:
            filename (str, optional): Sheet name. 단, None 인 경우 self.buf 사용 함.
        """
        self.buf = io.BytesIO()
        self.cells_format = defaultdict(dict)
        self.cols_format = []
        self.rows_format = []

        self.options = {**options}
        if not filename:
            self.options["in_memory"] = True

        self.workbook = xlsxwriter.Workbook(filename or self.buf, self.options)

    def write_worksheet(self, sheetname, data):
        """Write worksheet."""
        worksheet = self.workbook.add_worksheet(name=sheetname)

        for row_num, columns in enumerate(data):
            for col_num, cell_data in enumerate(columns):
                cell_format = self.cells_format[(row_num, col_num)]
                worksheet.write(
                    row_num,
                    col_num,
                    cell_data,
                    cell_format,
                )

        for col_format in self.cols_format:
            # https://xlsxwriter.readthedocs.io/worksheet.html#set_column_pixels
            worksheet.set_column_pixels(**col_format)

        for row_format in self.rows_format:
            worksheet.set_row(**row_format)

    def start(
        self,
        *sheets,
        sheetname=None,
        data=None,
        cells_format=None,
        cols_format=None,
        rows_format=None,
    ):
        """Start, write workbook.

        Args:
            *sheets (dict, optional): Multi sheet 작성하기.
            sheetname (str, optional): Sheet name.
            data (list(dict), optional): Sheet data.
            cells_format (dict|list(dict), optional): Sheet cells format.
            cols_format (dict|list(dict), optional): Sheet columns format.
            rows_format (dict|list(dict), optional): Sheet rows format.

        Examples:
            excel = Excel()
            excel.start(
                data=[[1,2,3], [4,5,6]]
                cols_format=[{"first_col": 0, "last_col": "0", "width": 100}],
                rows_format=[{"row": 0, "cell_format": {"bold": True}}],
            )
        """
        try:
            if cells_format:
                self.set_cells_format(**cells_format)

            if cols_format:
                if isinstance(cols_format, dict):
                    self.set_cols_format(**cols_format)
                else:
                    self.set_cols_format(*cols_format)

            if rows_format:
                if isinstance(rows_format, dict):
                    self.set_rows_format(**rows_format)
                else:
                    self.set_rows_format(*rows_format)

            if data:
                self.write_worksheet(sheetname or "Sheet1", data)
            else:
                for (i, worksheet_kwargs) in enumerate(sheets, start=1):
                    worksheet_kwargs["sheetname"] = (
                        worksheet_kwargs.get("sheetname") or f"Sheet{i}"
                    )
                    self.write_worksheet(**worksheet_kwargs)
        except ExcelError as e:
            raise ExcelError(*e.args) from e

        self.close()

    def set_cells_format(
        self, cells_format=None, positions=None, default_cell_format=None
    ):
        """Cells format 생성하기.

        Args:
            cells_format (list(dict)): 생성할 format 목록, for examples:
                [{}, ...]
            positions(list(tuple(int, int))): 생성할 format 목록의 cell 위치, for examples:
                [(0, 0), (0, 1), ...]
            default_cell_format (dict, optional): 기본 format. for examples:
                {}

        Examples:
            cells_format = [{"bold": True}]
            positions = [(0,0), (0, 1)]
            default_cell_format = {"bold": True}

        Returns:
            defaultdict(tuple: dict):
                defaultdict({
                    (0, 0): {"bold": True},
                    (0, 1): {"bold": True},
                })
        """
        for i, position in enumerate(positions or ()):
            try:
                cell_format = cells_format[i]
            except IndexError:
                cell_format = default_cell_format or {}
            if cell_format:
                cell_format = self.workbook.add_format(cell_format)
            self.cells_format[position] = cell_format

    def set_cols_format(
        self,
        *cols,
        first_col=None,
        last_col=None,
        width=100,
        cell_format=None,
        options=None,
    ):
        """Columns format 생성하기.

        Examples:
            cols = [{"first_col": 0, "last_col": 0, "width": 100}]

        References:
            https://xlsxwriter.readthedocs.io/worksheet.html#set_column
        """
        if first_col is not None:
            if cell_format:
                cell_format = self.workbook.add_format(cell_format)
            self.cols_format.append(
                {
                    "first_col": first_col,
                    "last_col": last_col,
                    "width": width,
                    "cell_format": cell_format,
                    "options": options or {},
                }
            )
        else:
            for col_kwargs in cols:
                cell_format = col_kwargs.get("cell_format")
                if cell_format:
                    cell_format = self.workbook.add_format(cell_format)
                self.cols_format.append({**col_kwargs, "cell_format": cell_format})

    def set_rows_format(
        self, *rows, row=None, height=15, cell_format=None, options=None
    ):
        """Rows format 생성하기.

        Examples:
            rows = [{"row": 0, "cell_format": {"bold": True}}]

        References:
            https://xlsxwriter.readthedocs.io/worksheet.html#set_row
        """
        if row is not None:
            if cell_format:
                cell_format = self.workbook.add_format(cell_format)
            self.rows_format.append(
                {
                    "row": row,
                    "height": height,
                    "cell_format": cell_format,
                    "options": options or {},
                }
            )
        else:
            for row_kwargs in rows:
                cell_format = row_kwargs.get("cell_format")
                if cell_format:
                    cell_format = self.workbook.add_format(cell_format)
                self.rows_format.append({**row_kwargs, "cell_format": cell_format})

    def close(self):
        """Close."""
        self.workbook.close()
        self.buf.seek(io.SEEK_SET)


class MIMETypeEnum(Enum):
    """MIME type with excel.

    References:
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types
    """

    def __new__(cls, mime_type, kind_of_document):
        """MIME type with excel __new__."""
        obj = object.__new__(cls)
        obj._value = mime_type
        obj.label = kind_of_document
        return obj

    @property
    def value(self):
        """MIME type with excel get value."""
        return self._value

    XLS = ("application/vnd.ms-excel", "Microsoft Excel")
    XLSX = (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "Microsoft Excel (OpenXML)",
    )
