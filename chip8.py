import pyxel
import random
import time

pyxel.init(64, 32, fps=4000)

global chip8, opcode

def pause():
    k = input()

chip8 = {
    "V": [0] * 16,
    "memory": [0] * 4096,
    "I":
    0,
    "delayTimer":
    0,
    "soundTimer":
    0,
    "PC":
    0x200,
    "SP":
    -1,
    "stack": [0] * 16,
    "keysDict": {
        0x0: pyxel.KEY_KP_0,
        0x1: pyxel.KEY_KP_1,
        0x2: pyxel.KEY_KP_2,
        0x3: pyxel.KEY_KP_3,
        0x4: pyxel.KEY_KP_4,
        0x5: pyxel.KEY_KP_5,
        0x6: pyxel.KEY_KP_6,
        0x7: pyxel.KEY_KP_7,
        0x8: pyxel.KEY_KP_8,
        0x9: pyxel.KEY_KP_9,
        0xA: pyxel.KEY_A,
        0xB: pyxel.KEY_B,
        0xC: pyxel.KEY_C,
        0xD: pyxel.KEY_D,
        0xE: pyxel.KEY_E,
        0xF: pyxel.KEY_F,
    },
    "displayMemory": [0] * (64 * 32),
    "fonts": [
        0xF0,
        0x90,
        0x90,
        0x90,
        0xF0,  #// 0
        0x20,
        0x60,
        0x20,
        0x20,
        0x70,  #// 1
        0xF0,
        0x10,
        0xF0,
        0x80,
        0xF0,  #// 2
        0xF0,
        0x10,
        0xF0,
        0x10,
        0xF0,  #// 3
        0x90,
        0x90,
        0xF0,
        0x10,
        0x10,  #// 4
        0xF0,
        0x80,
        0xF0,
        0x10,
        0xF0,  #// 5
        0xF0,
        0x80,
        0xF0,
        0x90,
        0xF0,  #// 6
        0xF0,
        0x10,
        0x20,
        0x40,
        0x40,  #// 7
        0xF0,
        0x90,
        0xF0,
        0x90,
        0xF0,  #// 8
        0xF0,
        0x90,
        0xF0,
        0x10,
        0xF0,  #// 9
        0xF0,
        0x90,
        0xF0,
        0x90,
        0x90,  #// A
        0xE0,
        0x90,
        0xE0,
        0x90,
        0xE0,  #// B
        0xF0,
        0x80,
        0x80,
        0x80,
        0xF0,  #// C
        0xE0,
        0x90,
        0x90,
        0x90,
        0xE0,  #// D
        0xF0,
        0x80,
        0xF0,
        0x80,
        0xF0,  #// E
        0xF0,
        0x80,
        0xF0,
        0x80,
        0x80  #// F
    ]
}

opcode = 0

def getROM(memory, path):
    rom = open(path, 'rb')
    for index, val in enumerate(rom.read()):
        memory[0x200 + index] = val

#Loading Fonts
fontstart = 0x050
for i in chip8["fonts"]:
    chip8["memory"][fontstart] = i
    fontstart += 1
pong = "PONG"
test = "test_opcode.ch8"
getROM(chip8["memory"], pong)
#print(chip8["memory"])

def fetch():
    opcode = chip8["memory"][chip8["PC"]] << 8 | chip8["memory"][chip8["PC"] +
                                                                 1]
    chip8["PC"] += 2
    return opcode

def decode(opcode):
    #print(opcode)
    global arg_a, arg_x, arg_y, arg_xnnn, arg_xxnn, arg_xxxn
    arg_a = (opcode & 0xf000) >> 12
    arg_x = (opcode & 0x0f00) >> 8
    arg_y = (opcode & 0x00f0) >> 4
    arg_xnnn = opcode & 0x0fff
    arg_xxnn = opcode & 0x00ff
    arg_xxxn = opcode & 0x000f
    #print("=================================")
    #print(arg_a,arg_x,arg_xnnn,arg_xxnn,arg_xxxn,arg_y)
    #print("=================================")
    if opcode == 0x00e0:
        return "CLS"
    elif opcode == 0x00ee:
        return "RET"
    elif arg_a == 1:
        return "JP addr"
    elif arg_a == 2:
        return "CALL addr"
    elif arg_a == 3:
        return "SE Vx, byte"
    elif arg_a == 4:
        return "SNE Vx, byte"
    elif arg_a == 5:
        return "SE Vx, Vy"
    elif arg_a == 6:
        return "LD Vx, byte"
    elif arg_a == 7:
        return "ADD Vx, byte"
    elif arg_a == 8:
        if arg_xxxn == 0:
            return "LD Vx, Vy"
        elif arg_xxxn == 1:
            return "OR Vx, Vy"
        elif arg_xxxn == 2:
            return "AND Vx, Vy"
        elif arg_xxxn == 3:
            return "XOR Vx, Vy"
        elif arg_xxxn == 4:
            return "ADD Vx, Vy"
        elif arg_xxxn == 5:
            return "SUB Vx, Vy"
        elif arg_xxxn == 6:
            return "SHR Vx, Vy"
        elif arg_xxxn == 7:
            return "SUBN Vx, Vy"
        elif arg_xxxn == 14:
            return "SHL Vx, Vy"
    elif arg_a == 9:
        return "SNE Vx, Vy"
    elif arg_a == 10:
        return "LD I, addr"
    elif arg_a == 11:
        return "JP V0, addr"
    elif arg_a == 12:
        return "RND Vx, byte"
    elif arg_a == 13:
        return "DRW Vx, Vy, nibble"
    elif arg_a == 14:
        if arg_xxnn == 0x9e:
            return "SKP Vx"
        elif arg_xxnn == 0xa1:
            return "SKNP Vx"
    elif arg_a == 15:
        if arg_xxnn == 0x07:
            return "LD Vx, DT"
        elif arg_xxnn == 0x0a:
            return " LD Vx, K"
        elif arg_xxnn == 0x15:
            return "LD DT, Vx"
        elif arg_xxnn == 0x18:
            return "LD ST, Vx"
        elif arg_xxnn == 0x1e:
            return "ADD I, Vx"
        elif arg_xxnn == 0x29:
            return "LD F, Vx"
        elif arg_xxnn == 0x33:
            return "LD B, Vx"
        elif arg_xxnn == 0x55:
            return "LD [I], Vx"
        elif arg_xxnn == 0x65:
            return "LD Vx, [I]"

def setPixel(x, y):
    cols = 64
    rows = 32
    print(x, y)
    if x > cols:
        x -= cols
    elif x < 0:
        x += cols
    if y > rows:
        y -= rows
    elif y < 0:
        y += rows
    pixelIndex = x + y * cols
    print(pixelIndex)
    chip8["displayMemory"][pixelIndex] ^= 1
    return not chip8["displayMemory"][pixelIndex]

def execute(s):
    #print("Did ", s)
    if s == "CLS":
        chip8["displayMemory"] = [0] * (64 * 32)
    elif s == "RET":
        chip8["PC"] = chip8["stack"].pop()
    elif s == "JP addr":
        addr = arg_xnnn
        chip8["PC"] = addr
    elif s == "CALL addr":
        addr = arg_xnnn
        chip8["stack"].append(chip8["PC"])
        chip8["PC"] = addr
    elif s == "SE Vx, byte":
        Vx = arg_x
        byte = arg_xxnn
        if chip8["V"][Vx] == byte:
            chip8["PC"] += 2
    elif s == "SNE Vx, byte":
        Vx = arg_x
        byte = arg_xxnn
        if chip8["V"][Vx] != byte:
            chip8["PC"] += 2
    elif s == "SE Vx, Vy":
        Vx = arg_x
        Vy = arg_y
        if chip8["V"][Vx] == chip8["V"][Vy]:
            chip8["PC"] += 2
    elif s == "LD Vx, byte":
        Vx = arg_x
        byte = arg_xxnn
        chip8["V"][Vx] = byte
    elif s == "ADD Vx, byte":
        Vx = arg_x
        byte = arg_xxnn
        result = (chip8["V"][Vx] + byte)
        result = result % 256
        chip8["V"][Vx] = result
    elif s == "LD Vx, Vy":
        Vx = arg_x
        Vy = arg_y
        chip8["V"][Vx] = chip8["V"][Vy]
    elif s == "OR Vx, Vy":
        Vx = arg_x
        Vy = arg_y
        chip8["V"][Vx] = chip8["V"][Vx] | chip8["V"][Vy]
    elif s == "AND Vx, Vy":
        Vx = arg_x
        Vy = arg_y
        chip8["V"][Vx] = chip8["V"][Vx] & chip8["V"][Vy]
    elif s == "XOR Vx, Vy":
        Vx = arg_x
        Vy = arg_y
        chip8["V"][Vx] = chip8["V"][Vx] ^ chip8["V"][Vy]
    elif s == "ADD Vx, Vy":
        Vx = arg_x
        Vy = arg_y
        add = chip8["V"][Vx] + chip8["V"][Vy]
        if add > 255:
            chip8["V"][15] = 1
        else:
            chip8["V"][15] = 0
        chip8["V"][Vx] = add % 256
    elif s == "SUB Vx, Vy":
        Vx = arg_x
        Vy = arg_y
        sub = chip8["V"][Vx] - chip8["V"][Vy]
        if sub > 0:
            chip8["V"][15] = 1
        else:
            chip8["V"][15] = 0
        chip8["V"][Vx] = sub % 256
    elif s == "SHR Vx, Vy":
        Vx = arg_x
        Vy = arg_y
        chip8["V"][15] = chip8["V"][Vx] & 0x1
        print(chip8["V"][Vx])
        chip8["V"][Vx] = (chip8["V"][Vx] >> 1) % 255
        print(chip8["V"][Vx])
        """
        val = chip8["V"][Vx]
        lsb = val & 0x1
        chip8["V"][15] = lsb
        chip8["V"][Vx] = val >> 1
        """
        """
        if chip8["V"][Vx] & 0x1 == 1:
            chip8["V"][15] = 1
        else:
            chip8["V"][15] = 0
        print(chip8["V"][Vx])
        chip8["V"][Vx] = chip8["V"][Vx] >> 1
        """
    elif s == "SUBN Vx, Vy":
        Vx = arg_x
        Vy = arg_y
        val = chip8["V"][Vx] - chip8["V"][Vy]
        if val > 0:
            chip8["V"][15] = 1
        else:
            chip8["V"][15] = 0
        chip8["V"][Vx] = val
    elif s == "SHL Vx, Vy":
        Vx = arg_x
        Vy = arg_y
        chip8["V"][15] = chip8["V"][Vx] & 0x80
        print(chip8["V"][Vx])
        chip8["V"][Vx] = chip8["V"][Vx] << 1
        print(chip8["V"][Vx])
        """
        Vx = arg_x
        if chip8["V"][Vx] & 0x80 == 1:
            chip8["V"][15] = 1
        else:
            chip8["V"][15] = 0
        chip8["V"][Vx] = chip8["V"][Vx] << 1
        """
    elif s == "SNE Vx, Vy":
        Vx = arg_x
        Vy = arg_y
        #print(Vx, Vy)
        if chip8["V"][Vx] != chip8["V"][Vy]:
            chip8["PC"] += 2
    elif s == "LD I, addr":
        addr = arg_xnnn
        chip8["I"] = addr
    elif s == "JP V0, addr":
        addr = arg_xnnn
        chip8["PC"] = addr + chip8["V"][0]
    elif s == "RND Vx, byte":
        Vx = arg_x
        byte = arg_xxnn
        x = random.randint(0, 255)
        chip8["V"][Vx] = x & byte
    elif s == "DRW Vx, Vy, nibble":
        width = 8
        height = arg_xxxn
        Vx = arg_x
        Vy = arg_y
        chip8["V"][15] = 0
        for row in range(0, height):
            sprite = chip8["memory"][chip8["I"] + row]
            for col in range(0, width):
                if (sprite & 0x80) > 0:
                    if setPixel(chip8["V"][Vx] + col, chip8["V"][Vy] + row):
                        chip8["V"][15] = 1
                sprite = sprite << 1
    elif s == "SKP Vx":
        Vx = arg_x
        #print(chip8["V"][Vx])
        #print(chip8["keysDict"][chip8["V"][Vx]])
        if chip8["keysDict"][chip8["V"][Vx]]:
            chip8["PC"] += 2
    elif s == "SKNP Vx":
        Vx = arg_x
        #print(chip8["V"][Vx])
        #print(chip8["keysDict"][chip8["V"][Vx]])
        if not (chip8["keysDict"][chip8["V"][Vx]]):
            chip8["PC"] += 2
    elif s == "LD Vx, DT":
        Vx = arg_x
        chip8["V"][Vx] = chip8["delayTimer"]
    elif s == "LD Vx, K":
        Vx = arg_x
        for i in chip8["keysDict"]:
            if chip8["keysDict"][i]:
                chip8["V"][Vx] = i
                break
        else:
            chip8["PC"] -= 2
    elif s == "LD DT, Vx":
        Vx = arg_x
        chip8["delayTimer"] = chip8["V"][Vx]
    elif s == "LD ST, Vx":
        Vx = arg_x
        chip8["soundTimer"] = chip8["V"][Vx]
    elif s == "ADD I, Vx":
        Vx = arg_x
        chip8["I"] += Vx
    elif s == "LD F, Vx":
        Vx = arg_x
        digit = chip8["V"][Vx]
        chip8["I"] = 0x050 + 5 * digit
    elif s == "LD B, Vx":
        Vx = arg_x
        chip8["memory"][chip8["I"]] = chip8["V"][Vx] // 100
        chip8["memory"][chip8["I"] + 1] = (chip8["V"][Vx] % 100) // 10
        chip8["memory"][chip8["I"] + 2] = (chip8["V"][Vx] % 100) % 10
    elif s == "LD [I], Vx":
        Vx = arg_x
        loc = chip8["I"]
        for i in range(0, Vx + 1):
            chip8["memory"][loc] = chip8["V"][i]
            loc += 1
    elif s == "LD Vx, [I]":
        Vx = arg_x
        loc = chip8["I"]
        for i in range(0, Vx + 1):
            chip8["V"][i] = chip8["memory"][loc]
            loc += 1

    #print(chip8)
    #pause()
def cpucycle():
    k = fetch()
    m = decode(k)
    execute(m)
    time.sleep(1 / 60)
    if chip8["delayTimer"] > 0:
        chip8["delayTimer"] -= 1
        """
    if chip8["soundTimer"] > 0:
        if chip8["soundTimer"] == 1:
            pyxel.sound(0)
        chip8["delayTimer"] -= 1"""


def update():
    running = True
    """while chip8["delayTimer"]:
        time.sleep(1/60)
        chip8["delayTimer"] -= 1"""
    chip8["keysDict"] = {
        0x0: pyxel.btn(pyxel.KEY_KP_0),
        0x1: pyxel.btn(pyxel.KEY_KP_1),
        0x2: pyxel.btn(pyxel.KEY_KP_2),
        0x3: pyxel.btn(pyxel.KEY_KP_3),
        0x4: pyxel.btn(pyxel.KEY_KP_4),
        0x5: pyxel.btn(pyxel.KEY_KP_5),
        0x6: pyxel.btn(pyxel.KEY_KP_6),
        0x7: pyxel.btn(pyxel.KEY_KP_7),
        0x8: pyxel.btn(pyxel.KEY_KP_8),
        0x9: pyxel.btn(pyxel.KEY_KP_9),
        0xA: pyxel.btn(pyxel.KEY_A),
        0xB: pyxel.btn(pyxel.KEY_B),
        0xC: pyxel.btn(pyxel.KEY_C),
        0xD: pyxel.btn(pyxel.KEY_D),
        0xE: pyxel.btn(pyxel.KEY_E),
        0xF: pyxel.btn(pyxel.KEY_F)
    }
    #print(chip8["keysDict"])
    cpucycle()
    print(pyxel.btnp(pyxel.KEY_Q))
    if pyxel.btn(pyxel.KEY_Q) and running:
        print(pyxel.btnp(pyxel.KEY_Q))
        pyxel.quit()

def draw():
    #pyxel.cls(0)
    for i in range(0, len(chip8["displayMemory"])):
        #print(i)
        if chip8["displayMemory"][i] == 1:
            z = 11
        else:
            z = 1
        x = (i) % 64
        y = (i) // 64
        #print(x,y)
        pyxel.pset(x, y, z)
    #pyxel.pset(10,10,11)
    #pyxel.rect(10, 10, 20, 20, 11)

pyxel.run(update, draw)
