# Image-formatter: MkDocs plugin for easier management of image sizes

#### This plugin is being developed as part of Advanced Programming in Python course (23L edition)

### Team members:

- Mateusz Wasilewski
- Aleksandra Sypuła
- Julia Jodczyk

### Description:

The plugin allows you to define image size categories and use them as tags in your documentation. The images annotated with tags will be resized to the size specified in the configuration file.

### (Planned) Usage:

#### Step 1.

To configuration file add:

```
- image_sizes:
    - <tag_name>:
        width: <size>
        height: <size>
    - <tag_name>:
        width: <size>
        height: <size>
```

where different `tag_names` are the names of image size categories. Remember about measurement units (`px, %, etc.`) when specifying width and height.

Example of correct configuration:

```
- image_sizes:
    - large:
        width: 100px
        height: 50px
    - small:
        width: 80px
        height: 40px
```

#### Step 2:

Annotate images in your documents with desired tags.

Example:

```
@small
(../images/b.png)
```
