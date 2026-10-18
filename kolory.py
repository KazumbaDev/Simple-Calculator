while True:
    r = int(input("r: "))
    g = int(input("g: "))
    b = int(input("b: "))
#    a = int(input("a: "))

    def rgb_to_kivy(r, g, b, a=1):

        print(r / 255, g / 255, b / 255, a)

    rgb_to_kivy(r, g, b)