class ImageVersion:
    def __init__(self, image_full_version: str, image_type: str):
        self.image_full_version = image_full_version
        self.image_type = image_type
        self.major_version = image_full_version.split(".")[0]
        self.minor_version = image_full_version.split(".")[1]
        self.patch_version = image_full_version.split(".")[2]

    # 1.11.0, 1.11.0
    def full_version(self):
        return self.image_full_version

    # 1.11, 1.11
    def major_minor(self):
        return self.major_version + "." + self.minor_version

    # 1.11.0-cpu, 1.11.0-gpu
    def full_version_with_type(self):
        return self.image_full_version + "-" + self.image_type

    # 1.11-cpu, 1.11-gpu
    def major_minor_with_type(self):
        return self.major_version + "." + self.minor_version + "-" + self.image_type

    # 1-cpu, 1-gpu
    def major_with_type(self):
        return self.major_version + "-" + self.image_type
