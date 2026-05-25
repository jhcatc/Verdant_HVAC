export async function getEquipmentDocuments(
    equipmentId: string
) {

    const res = await fetch(
        `/api/hvac/equipment/${equipmentId}/documents`
    );

    if (!res.ok) {
        throw new Error(
            'Failed loading documents'
        );
    }

    return await res.json();
}

export async function uploadEquipmentDocument(
    equipmentId: string,
    file: File
) {

    const form = new FormData();

    form.append('file', file);

    const res = await fetch(
        `/api/hvac/equipment/${equipmentId}/documents`,
        {
            method: 'POST',
            body: form
        }
    );

    if (!res.ok) {
        throw new Error(
            'Failed uploading document'
        );
    }

    return await res.json();
}