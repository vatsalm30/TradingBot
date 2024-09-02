def confidence_to_color(confidence):
    # Ensure confidence is within bounds [0, 1]
    confidence = max(0.0, min(confidence, 1.0))

    # RGB values for red and blue
    red_rgb = (255, 0, 0)   # #FF0000
    blue_rgb = (0, 0, 255)  # #0000FF

    # Interpolate between red and blue based on confidence
    r = int(blue_rgb[0] + (red_rgb[0] - blue_rgb[0]) * confidence)
    g = int(blue_rgb[1] + (red_rgb[1] - blue_rgb[1]) * confidence)
    b = int(blue_rgb[2] + (red_rgb[2] - blue_rgb[2]) * confidence)

    # Convert RGB to hex
    color_hex = "#{:02X}{:02X}{:02X}".format(r, g, b)
    
    return color_hex
