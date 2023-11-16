import os
from os import getcwd
from typing import List

from fastapi import APIRouter, UploadFile, File
from starlette.responses import FileResponse
import numpy as np
from PIL import Image, ImageDraw

router = APIRouter()


@router.get("/")
def get_file(name_file: str, directory: str = "publication"):
    path = getcwd() + f"/files/{directory}/{name_file}"
    if os.path.exists(path):
        return FileResponse(path=path)


@router.post("/")
async def create_upload_file(
    *,
    uploaded_files: List[UploadFile] = File(...),
    directory: str = "publication"
    # current_user: models.User = Depends(deps.get_current_active_user)
):
    for uploaded_file in uploaded_files:
        name = uploaded_file.filename
        file_location = f"files/{directory}/{str(name).replace(' ', '_')}"
        with open(file_location, "wb+") as file_object:
            file_object.write(uploaded_file.file.read())
        if directory == "photo":
            extension = list(os.path.splitext(uploaded_file.filename))[1]
            photo = list(os.path.splitext(uploaded_file.filename))[0]
            new_path = f"files/{directory}/{photo.replace(' ', '_')}.png"
            convert_photo(file_location, new_path, extension)
            return {"filenames": [f"{photo}.png"]}
    return {
        "filenames": [str(file.filename).replace(" ", "_") for file in uploaded_files]
    }


@router.post("/image")
async def create_upload_file(
    *,
    uploaded_file: UploadFile = File(...),
    directory: str = "product_image",
    # current_user: models.User = Depends(deps.get_current_active_user)
):
    name = uploaded_file.filename
    file_location = f"files/{directory}/{str(name).replace(' ', '_')}"

    output_thumbnail_path = f"files/product_thumbnail/{str(name).replace(' ', '_')}"
    with open(file_location, "wb+") as file_object:
        file_object.write(uploaded_file.file.read())
    create_thumbnail(file_location, output_thumbnail_path)
    return {"filenames": f"{uploaded_file.filename.replace(' ', '_')}"}


def convert_photo(path: str, new_path: str, extension):
    # Open the input image as numpy array, convert to RGB
    img = Image.open(path).convert("RGB")
    npImage = np.array(img)
    h, w = img.size

    # Create same size alpha layer with circle
    alpha = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(alpha)
    draw.pieslice([0, 0, h, w], 0, 360, fill=255)

    # Convert alpha Image to numpy array
    npAlpha = np.array(alpha)

    # Add alpha layer to RGB
    npImage = np.dstack((npImage, npAlpha))

    # Save with alpha
    Image.fromarray(npImage).save(new_path)
    if os.path.exists(new_path) and extension != ".png":
        os.remove(path)


def create_thumbnail(
    input_image_path, output_thumbnail_path, thumbnail_size=(100, 100)
):
    with Image.open(input_image_path) as img:
        # Create a thumbnail with the specified size
        thumbnail = img.copy()
        thumbnail.thumbnail(thumbnail_size)

        # Save the thumbnail
        thumbnail.save(
            output_thumbnail_path, "jpeg"
        )  # You can change the format if needed
    return output_thumbnail_path
