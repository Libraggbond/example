#enc = "105-61-35-38-247-15-18-6-233-213-215-181-178-112-137-125-99-30-67-63-45-46-30"
enc = "49-97-65-74-0-7-243-232-254-238"

enc_array = enc.split('-')


def move(arr):
    result = []
    for i in range(len(arr)):
        res = int(arr[i]) + i * 16 % 256
        if res > 255:
            res = res - 256
        result.append(chr(res))
    return result

clear = move(enc_array)

b = "".join(clear)
print b[:-2]
