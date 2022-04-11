""""""
import json
from collections import defaultdict
from json.decoder import JSONDecodeError

from django.http.response import FileResponse
from django.views import View

from utils.xlsxwriter import Excel, MIMETypeEnum, execute_graphql_query


class DownloadsView(View):
    """Downloads django view."""

    def dispatch(self, request, *args, **kwargs):
        """Override."""
        if request.method.lower() in self.http_method_names:
            method = kwargs.get("method")
            handler = getattr(self, method, None)
        else:
            handler = None

        if handler:
            _kwargs = {**kwargs}
            for key, value in getattr(request, request.method).dict().items():
                if key in ["csrfmiddlewaretoken"]:
                    continue

                try:
                    _kwargs[key] = json.loads(value)
                except json.JSONDecodeError:
                    _kwargs[key] = value
        else:
            handler = self.http_method_not_allowed
            _kwargs = kwargs
        return handler(request, *args, **_kwargs)

    def excel(
        request,
        *args,
        title="",
        columns=None,
        query=None,
        variables=None,
        **kwargs,
    ):
        """Excel downloads."""
        # query 질의하기, data 가져오기.
        result = execute_graphql_query(query, **variables or {})

        # Row 서식 정의하기.
        rows_format = [
            {
                "row": 0,
                "cell_format": {
                    "align": "center",
                    "bold": True,
                    "bg_color": "#CCCCCC",
                    "valign": "center",
                },
            }
        ]

        # Column 서식 정의하기.
        cols_format = []

        # data 내에 특정 field 의 값을 가져오기 위한 fields 정의하기.
        fields = []

        # fields 의 label 을 나타내는 headers 정의하기.
        headers = []

        # data 내에 특정 field 의 값을 변경하기 위한 render 가공하기.
        renders = defaultdict(defaultdict)

        for i, col in enumerate(columns or []):
            cols_format.append(
                {
                    "first_col": i,
                    "last_col": i,
                    "width": col.get("width", 100),
                }
            )
            field = col["field"]
            fields.append(field)
            headers.append(col.get("header", ""))
            for key, value in col.get("render", {}).items():
                try:
                    renders[field][json.loads(key)] = value
                except JSONDecodeError:
                    renders[field][key] = value

        # data 가공하기.
        nodes = (
            edge["node"]
            for _, obj in result.data.items()
            for edge in obj.get("edges", [])
        )
        data = [headers]
        for node in nodes:
            row = []
            for field in fields:
                value = node[field]
                render = renders.get(field, {})
                row.append(render.get(node[field], value))
            data.append(row)

        # Excel 생성하기.
        _excel = Excel()
        _excel.start(
            data=data,
            cols_format=cols_format,
            rows_format=rows_format,
        )

        # 생성된 Excel 반환하기.
        return FileResponse(
            _excel.buf,
            as_attachment=True,
            filename=f"{title}.xlsx",
            headers={
                "Content-Type": MIMETypeEnum.XLSX.value,
            },
        )
