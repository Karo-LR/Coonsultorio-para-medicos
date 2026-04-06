from django.http import HttpResponse
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from core.models import Consulta
from core.permissions import get_user_role


def _escape_pdf_text(value):
    return value.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _build_simple_pdf(lines):
    content_lines = ["BT", "/F1 12 Tf", "40 750 Td", "16 TL"]
    for index, line in enumerate(lines):
        prefix = "" if index == 0 else "T* "
        content_lines.append(f"{prefix}({_escape_pdf_text(line)}) Tj")
    content_lines.append("ET")
    content_stream = "\n".join(content_lines).encode("latin-1", errors="replace")

    objects = []
    objects.append(b"1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n")
    objects.append(b"2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj\n")
    objects.append(
        b"3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        b"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >> endobj\n"
    )
    objects.append(b"4 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj\n")
    objects.append(
        f"5 0 obj << /Length {len(content_stream)} >> stream\n".encode("ascii")
        + content_stream
        + b"\nendstream endobj\n"
    )

    pdf = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for obj in objects:
        offsets.append(len(pdf))
        pdf.extend(obj)

    xref_offset = len(pdf)
    pdf.extend(f"xref\n0 {len(offsets)}\n".encode("ascii"))
    pdf.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode("ascii"))

    pdf.extend(
        (
            f"trailer << /Size {len(offsets)} /Root 1 0 R >>\n"
            f"startxref\n{xref_offset}\n%%EOF"
        ).encode("ascii")
    )
    return bytes(pdf)


class ConsultaPDFView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        consulta = Consulta.objects.select_related("cita", "cita__paciente", "cita__medico").get(pk=pk)
        role = get_user_role(request.user)

        if role == "recepcionista":
            raise PermissionDenied("No tienes permiso para ver informacion medica sensible.")

        if role == "doctor" and consulta.cita.medico_id != request.user.id:
            raise PermissionDenied("Solo puedes ver los PDF de tus propias consultas.")

        lines = [
            "Resumen de Consulta",
            "",
            f"Paciente: {consulta.cita.paciente}",
            f"Doctor: {consulta.cita.medico.get_full_name().strip() or consulta.cita.medico.username}",
            f"Fecha: {consulta.cita.fecha.strftime('%d/%m/%Y %H:%M')}",
            "",
            "Diagnostico:",
            consulta.diagnostico,
            "",
            "Tratamiento:",
            consulta.tratamiento,
        ]
        pdf_bytes = _build_simple_pdf(lines)
        response = HttpResponse(pdf_bytes, content_type="application/pdf")
        response["Content-Disposition"] = f'inline; filename="consulta-{consulta.id}.pdf"'
        return response
