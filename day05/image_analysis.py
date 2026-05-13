from PIL import Image

def analyze_image(composition_carpetplot):
    img = Image.open(composition_carpetplot)

    grayscale = img.convert("L")

    pixels = list(grayscale.getdata())

    average = sum(pixels) / len(pixels)

    darkest = min(pixels)

    brightest = max(pixels)

    bright_pixels = 0

    for pixel in pixels:
        if pixel > 200:
            bright_pixels += 1

    percent_bright = (bright_pixels / len(pixels)) * 100

    return average, darkest, brightest, percent_bright


if __name__ == "__main__":

    average, darkest, brightest, percent_bright = analyze_image(
        "composition_carpetplot.png"
    )

    print("Average intensity:", average)
    print("Darkest pixel:", darkest)
    print("Brightest pixel:", brightest)
    print("Percent bright pixels:", percent_bright)