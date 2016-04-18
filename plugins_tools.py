

def store_test_photo_helper(root_dir, image_paths):
    import tempfile
    import shutil
    import os

    TEST_PHOTO_PATH = os.path.join(root_dir, 'test_photo')
    if not os.path.exists(TEST_PHOTO_PATH):
        os.makedirs(TEST_PHOTO_PATH)

    TEST_IMAGE_FOLDER = tempfile.mkdtemp(dir=TEST_PHOTO_PATH)
    if not os.path.exists(TEST_IMAGE_FOLDER):
        os.makedirs(TEST_IMAGE_FOLDER)

    for path in image_paths:
        shutil.copyfile(path, os.path.join(TEST_IMAGE_FOLDER, os.path.basename(path)))
    return TEST_IMAGE_FOLDER
