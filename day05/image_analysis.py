from PIL import Image


def detect_composomes(image_file):

    # open image
    img = Image.open(image_file)

    # convert image to RGB
    img = img.convert("RGB")

    # image size
    width, height = img.size

    composomes = 0

    red_regions = 0
    non_red_regions = 0

    inside_composome = False

    # move along diagonal
    for i in range(width):

        red_total = 0
        blue_total = 0

        # check nearby pixels around diagonal
        for offset in range(-25, 25):

            x = i + offset
            y = i

            # skip invalid positions
            if x < 0 or x >= width:
                continue

            # get pixel color
            r, g, b = img.getpixel((x, y))

            red_total += r
            blue_total += b

        # strong red/yellow region
        if red_total > blue_total + 4000:

            red_regions += 1

            # count composome only once
            if not inside_composome:

                composomes += 1

                inside_composome = True

        else:

            non_red_regions += 1

            inside_composome = False

    return composomes, red_regions, non_red_regions


if __name__ == "__main__":

    composomes, red_regions, non_red_regions = detect_composomes(
        "composition_carpetplot.png"
    )

    print("Composomes detected:", composomes)

    print("Red diagonal regions:", red_regions)

    print("Non-red diagonal regions:", non_red_regions)