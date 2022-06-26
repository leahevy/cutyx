# 💡 Examples

This is an example how to use **CutyX**.

## Setup testing images

You can use the provided test images for testing purposes. Run the following command:

```bash
python tests/download_images.py
```

After that, ten example images will be available in `./tests/image-gallery`.

## Add images to an album

Now setup two albums with training data to use it with **cutyx**:

```bash
cutyx match faces ./tests/image-gallery/linus1.jpg albums/linus
cutyx match faces ./tests/image-gallery/einstein1.jpg albums/einstein
cutyx match faces ./tests/image-gallery/einstein2.jpg albums/einstein
cutyx match faces ./tests/image-gallery/stallman1.jpg albums/stallman
```

As you can see, you can add multiple faces to be classified for an album.

## Run the classifier and organiser

Run the following command:

```bash
cutyx run
```

Your albums sub-folders will contain the images with the matching faces.

## Cache

**CutyX** manages a cache to add new training faces with ease, without having to classify all
images again. The cache directory is located in the configured root directory (defaults to the
current directory).

To clear the cache run `cutyx clear-cache`.

You can also generate the cache without running anything else with `cutyx update-cache`.

If you specify the `-c` option to **CutyX**, no cache will be used and everything will be classified
during this run.

## Further options

To get insights on further options you can use with **CutyX** run the appropriate help commands,
e.g. `cutyx --help` or `cutyx run --help`.
