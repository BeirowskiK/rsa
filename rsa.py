import random

# RABIN-MILLER
def primeFactors(n):
    output = []
    i = 2
    while n > 1:
        if n % i == 0:
            output.append(i)
            n /= i
        i += 1
    output.sort()
    return output


def division(n):
    s = n - 1
    power = 0
    while s%2 != 1:
        s = s // 2
        power += 1
    result = {'power': power, 'number': s}
    return result


def nwd(a, b):
    c = 0
    y_a = 0
    y_b = 1
    x_a = 1
    x_b = 0

    while a * b != 0:
        if a >= b:
            c = a // b
            a = a % b
            x_a = x_a - (x_b * c)
            y_a = y_a - (y_b * c)
        else:
            c = b // a
            b = b % a
            x_b = x_b - (x_a * c)
            y_b = y_b - (y_a * c)

    if a > 0:
        x = x_a
        y = y_a
        nwd = a
    else:
        x = x_b
        y = y_b
        nwd = b
    return {'nwd': nwd, 'x': x, 'y': y}


def rabinMiller(n, p, s):
    a = random.randint(2, n-1)
    x = modPow(a, s, n)

    if x == 1 or x == n-1:
        return True
    else:
        for i in range(1, p):
            x = modPow(x, 2, n)

            if x == n-1:
                return True

        if x != n-1:
            return False
        else:
            return True


def modPow(a, k, m):
    result = 1
    while k > 0:
        if k % 2 == 1:
            result = (result * a) % m

        a = (a * a) % m
        k = k // 2

    return result


def mainRM(n, k):
    n = n
    k = k
    primary = True

    if n <= 1:
        primary = False

    elif n < 3:
        primary = True
    else:
        parts = division(n)
        i = 0

        while primary and i < k:
            primary = rabinMiller(n, parts['power'], parts['number'])
            i += 1

    if primary:
        return True
    else:
        return False


#RSA
def generateKey():
    print("Podaj długość klucza:")
    m = int(input())

    start = pow(2, m - 1)
    stop = pow(2, m)

    p = random.randint(start, stop + 1)
    q = random.randint(start, stop + 1)

    while mainRM(p, 5) != True:
        p = random.randint(start, stop + 1)

    while mainRM(q, 5) != True:
        q = random.randint(start, stop + 1)

    n = p * q
    phin = (p - 1) * (q - 1)

    e = random.randint(start, stop + 1)

    nwde = nwd(e, phin)
    while nwde['nwd'] != 1:
        e = random.randint(start, stop + 1)
        nwde = nwd(phin, e)

    if (nwde['y'] < 0):
        d = nwde['y'] + phin
    else:
        d = nwde['y']

    publicKey = {'e': e, 'n': n}
    privateKey = {'d': d, 'n': n}

    return {'publicKey': publicKey, 'privateKey': privateKey}



#RSA CIPHER
def modPow(a, k, m):
    result = 1
    while k != 0:
        if k % 2 == 1:
            result *= a

        a = a * a % m
        k = k // 2

    return result % m


def rsaCipher(x, e, n):
    cipher = modPow(x, e, n)
    return cipher


def rsaDecrypt(message, d, n):
    decrypted = modPow(message, d, n)
    return decrypted


def readData():
    print("Podaj wiadomość do zaszyfrowania:")
    message = input()
    return message

def menu():
    print("\nWybierz opcję:")
    print("1. Wygeneruj parę kluczy")
    print("2. Zaszyfruj tekst")
    print("3. Odszyfruj tekst")
    print("0. Zakończ program")
    option = input()
    return int(option)

def main():
    option = menu()
    while(option != 0):
        if option == 1:
            keys = generateKey()
            f = open("privatekey.txt", 'w')
            privateKey = str(keys['privateKey']['d']) + ',' + str(keys['privateKey']['n'])
            f.write(privateKey)
            f.close()

            f = open("publickey.txt", 'w')
            publicKey = str(keys['publicKey']['e']) + ',' + str(keys['publicKey']['n'])
            f.write(publicKey)
            f.close()

            print("KLUCZ PUBLICZY: ", publicKey)
            print("KLUCZ PRYWATNY: ", privateKey)
            print("=========================")
            print("KLUCZE ZAPISANO W PLIKACH")
            print("=========================")

        elif option == 2:
            f = open('publickey.txt', 'r')
            publicKey = f.readline().split(',')
            f.close()
            if len(publicKey) < 2:
                print("================================")
                print("BRAK KLUCZA PUBLICZNEGO W PLIKU!")
                print("================================")

                option = menu()
                continue
            else:
                cipherMsg = []
                message = readData()
                for letter in message:
                    cipherMsg.append(int(rsaCipher(ord(letter), int(publicKey[0]), int(publicKey[1]))))
                print("ZASZYFROWANA WIADOMOŚĆ: ", cipherMsg)

                msg = ''
                for item in cipherMsg:
                    msg += str(item) + ','
                msg = msg[:len(msg)-1]
                f = open("ciphermsg.txt", 'w')
                f.write(msg)
                f.close()
                print("=========================")
                print("WIADOMOŚĆ ZAPISANO W PLIKU")
                print("=========================")
        elif option == 3:
            f = open('privatekey.txt', 'r')
            privateKey = f.readline().split(',')
            f.close()
            if len(privateKey) < 2:
                print("===============================")
                print("BRAK KLUCZA PRYWATNEGO W PLIKU!")
                print("===============================")

                option = menu()
                continue
            else:
                f = open('ciphermsg.txt', 'r')
                cipherMsg = f.read().split(',')
                f.close()
                if len(cipherMsg) < 1:
                    print("================================")
                    print("BRAK WIADOMOŚCI DO ODSZYFROWANIA")
                    print("================================")
                else:
                    decryptedMsg = ''
                    for letter in cipherMsg:
                        decryptedMsg += chr(rsaDecrypt(int(letter), int(privateKey[0]), int(privateKey[1])))
                    print("ODSZYFROWANA WIADOMOŚĆ: ", decryptedMsg)

                    f = open("deciphermsg.txt", 'w')
                    f.write(decryptedMsg)
                    f.close()
                    print("=========================")
                    print("WIADOMOŚĆ ZAPISANO W PLIKU")
                    print("=========================")
        option = menu()

main()