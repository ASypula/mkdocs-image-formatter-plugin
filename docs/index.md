# Image-formatter: MkDocs plugin for easier management of image sizes

#### This plugin is being developed as part of Advanced Programming in Python course (23L edition)

### Team members:

- Mateusz Wasilewski
- Aleksandra Sypuła
- Julia Jodczyk

### Description:

The plugin allows you to define image size categories and use them as tags in your documentation. The images annotated with tags will be resized to the size specified in the configuration file.

### Usage:

#### Prerequisites
Plugin works by replacing your tags with attribute list that is later interpreted by `attr_list` markdown extension. Make sure you add it to `mkdocs.yaml` like so:
```
markdown_extensions:
  - attr_list
```

#### Step 1.

To configuration file add:

```
- image_formatter:
    image_size:
        <tag_name>:
            width: <size>
            height: <size>
        <tag_name>:
            width: <size>
            height: <size>
```

where different `tag_names` are the names of image size categories. Remember about measurement units (`px, %, etc.`) when specifying width and height.

Example of correct configuration:

```
markdown_extensions:
    - attr_list

plugins:
    - image-formatter:
        image_size:
            small:
                height: 100px
                width: 100px
            big:
                height: 200px
                width: 200px
```

#### Step 2:

Annotate images in your documents with desired tags.

Example:

```
![MyImage]@small(../images/b.png)
```

#### Info:
If you accidentally use a tag that is not specified in the documentation, the tag will be removed and the image will be displayed with no additional formatting.

