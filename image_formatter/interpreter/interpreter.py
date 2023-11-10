class Interpreter:
    def __init__(self, image_tags_properties: dict):
        """
        Class interpreter responsible for analyzing tokens in order to append properties for image urls.
        """
        self.image_tags_properties = dict()
        self.required_properties = {"width", "height"}
        self.set_image_tags_properties(image_tags_properties)

    def set_image_tags_properties(self, image_tags_properties: dict) -> None:
        """
        Sets new value for image_tags_properties if given values is valid.
        """
        if self.are_image_tags_properties_valid(image_tags_properties):
            self.image_tags_properties = image_tags_properties

    def are_image_tags_properties_valid(self, image_tags_properties: dict) -> bool:
        """
        Checks whether given image tags properties contain all required attributes / properties.
        """
        try:
            for tag_name, properties in image_tags_properties.items():
                if type(properties) != dict:
                    return False
                for p in self.required_properties:
                    if p not in properties.keys():
                        return False
                return True
        except ValueError:
            return False
