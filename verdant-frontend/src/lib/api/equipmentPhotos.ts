export async function getEquipmentPhotos(
    equipmentId: string
) {

    const res = await fetch(
        `/api/hvac/equipment/${equipmentId}/photos`
    );

    if (!res.ok) {

        throw new Error(
            'Failed loading photos'
        );
    }

    return await res.json();
}

export async function uploadEquipmentPhoto(
    equipmentId: string,
    file: File
) {

    const form = new FormData();

    form.append('file', file);

    const res = await fetch(
        `/api/hvac/equipment/${equipmentId}/photos`,
        {
            method: 'POST',
            body: form
        }
    );

    if (!res.ok) {

        throw new Error(
            'Failed uploading photo'
        );
    }

    return await res.json();
}