import io
import qrcode

from uuid import UUID

from fastapi.responses import StreamingResponse


def generate_equipment_qr(
    equipment_id: UUID
):

    qr_value = (
        f"equipment:{equipment_id}"
    )

    qr = qrcode.make(
        qr_value
    )

    buffer = io.BytesIO()

    qr.save(
        buffer,
        format="PNG"
    )

    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="image/png"
    )

