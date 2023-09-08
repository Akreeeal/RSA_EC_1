import random
from sympy import isprime, randprime
from math import gcd
from fractions import Fraction

encoding_dict = {
            'а': 10, 'б': 11, 'в': 12, 'г': 13, 'д': 14, 'е': 15, 'ё': 16, 'ж': 17, 'з': 18, 'и': 19,
            'й': 20, 'к': 21, 'л': 22, 'м': 23, 'н': 24, 'о': 25, 'п': 26, 'р': 27, 'с': 28, 'т': 29,
            'у': 30, 'ф': 31, 'х': 32, 'ц': 33, 'ч': 34, 'ш': 35, 'щ': 36, 'ъ': 37, 'ы': 38, 'ь': 39,
            'э': 40, 'ю': 41, 'я': 42, '.': 43, ',': 44, ' ': 45, '?': 46
        }

def RSA_key():
    #r = randprime(1, 1000)
    r = 37
    #q = randprime(1, 1000)
    q = 53
    N = r * q
    phi = (r - 1) * (q - 1)
    #e = random.randint(1, phi)
    e = 37
    while gcd(e, phi) != 1:
        e = random.randint(1, 20)
    d = pow(e, -1, phi)
    public_key = (N, e)
    private_key = (N, d)
    return public_key, private_key



def points(text, RSA_public_key, ell_points):
    result = []
    for i in text:
        x = pow(int(i),RSA_public_key[1],RSA_public_key[0])
        result.append(x)
    new_list = []
    for x in result:
        k = 0
        while x not in [point[0] for point in ell_points]:
            x += 1
            k += 1

        for point in ell_points:
            if point[0] == x:
                new_list.append([k, point[0], point[1]])
                break
    return new_list



def ell_main():
    print('ЭЛЛИПТИЧЕСКАЯ КРИВАЯ y^2 =x^3 +  ax +b (mod p)')
    a = random.randint(1, 100) # Случайное значение a от 1 до 100
    a = 154
    b = random.randint(1, 100) # Случайное значение b от 1 до 100
    b = 187
    p = randprime(1, 10000) # Случайное значение p от 100 до 1000
    p = 5431

    while not isprime(p):  # Проверка на простоту
        p = random.randint(1, 100000)
    if ((-4*a**3+27*b**2)==0):
        print('Кривая особая.Введите другие параметры.')
        a = random.randint(1, 100)
        b = random.randint(1, 100)
        p = random.randint(100, 1000)
        while not isprime(p):  # Проверка на простоту
            p = random.randint(100, 1000)
    else:
        def point_ell(x, y):  # Принадлежность
            if (y ** 2 - x ** 3 - a * x - b) % p == 0:
                return 1
            else:
                return 0
        print(a,b,p)
        def ell(): # Нахождение всех точек эллиптической кривой
            A = range(0, p)
            Ell = []
            for x in A:
                B = [y for y in A if (y ** 2 - x ** 3 - a * x - b) % p == 0]
                if len(B) != 0:
                    for y in B:
                        if point_ell(x,y):
                            Ell.append([x, y])
            return Ell

        ell_points = ell()
        #print(ell_points)
        G = random.choice(ell_points)
        #G = [2823, 5139]
        print(f"Генерирующая точка: G = {G}") # Генерация генерирующей точки

        n = len(ell()) + 1
        print(f'Порядок кривой: n = {n}') # Порядок кривой
        print()

        def EC_Key():
            s = randprime(1, p)
            while s == n:
                s = randprime(1, p)
            public_key = multiply_ell(G[0],G[1],s)
            private_key = s
            return public_key, private_key


        def summa_ell(Px, Py, Qx, Qy):  # Сложение
            if [Px, Py] == [None, None]:  # Точка в бесконечности - нейтральный элемент по сложению
                return [Qx, Qy]
            if [Qx, Qy] == [None, None]:
                return [Px, Py]
            if Px == Qx and Py == Qy:
                return double_ell(Px, Py)  # Удвоение
            if Px == Qx:
                if Qy == (-Py) % p:
                    return [None, None]  # точка в бесконечности
                if Py == Qy and Py % p != 0:
                    f = Fraction((3 * Px * Px + a) % p, (2 * Py) % p)
            else:
                f = Fraction((Py - Qy) % p, (Px - Qx) % p)
            alfa = (f.numerator * pow(f.denominator, -1, p)) % p
            x = (alfa ** 2 - Px - Qx) % p
            y = (alfa * (Px - x) - Py) % p
            return [x, y]

        def double_ell(Px, Py):
            if Py == 0:
                return [None, None]  # точка в бесконечности
            f = Fraction((3 * Px * Px + a) % p, (2 * Py) % p)
            alfa = (f.numerator * pow(f.denominator, -1, p)) % p
            x = (alfa ** 2 - 2 * Px) % p
            y = (alfa * (Px - x) - Py) % p
            return [x, y]

        def multiply_ell(Px, Py, n):
            Qx, Qy = None, None
            R = [Px, Py]
            for i in bin(n)[2:]:
                Qx, Qy = summa_ell(Qx, Qy, Qx, Qy)  # удвоение точки
                if i == '1':
                    Qx, Qy = summa_ell(Qx, Qy, R[0], R[1])  # сложение точек
            return Qx, Qy

        def main_ell():
            print(EC_Key())
            print('Выберите операцию:')
            print('1. Нахождение кратной точки')
            print('2. Операции сложения/удвоения точки')
            choice = int(input('Введите номер операции: '))
            if choice == 1:
                print('Координаты точки P:')
                Px = int(input('x='))
                Py = int(input('y='))
                print('Коэфицент n')
                n = int(input('n='))
                print(multiply_ell(Px,Py,n))
            elif choice == 2:
                print('Координаты точки P:')
                Px = int(input('x='))
                Py = int(input('y='))
                print('Координаты точки Q:')
                Qx = int(input('x='))
                Qy = int(input('y='))
                print(summa_ell(Px, Py, Qx, Qy))

        def RSA_key():
            r = randprime(100, p)
            #r = 37
            q = randprime(100, p)
            #q = 53
            N = r * q
            while N > p:
                r = randprime(1, p)
                q = randprime(1, p)
                N = r * q
            phi = (r - 1) * (q - 1)
            e = random.randint(1, phi)
            #e = 37
            while gcd(e, phi) != 1:
                e = random.randint(1, phi)
            d = pow(e, -1, phi)
            public_key = (N, e)
            private_key = (N, d)
            return public_key, private_key

        def encode_text(encoding_dict):
            text = input('Введите текст для кодирования: ')
            encoded_text = []
            for char in text:
                char = char.lower()
                if char in encoding_dict:
                    encoded_text.append(str(encoding_dict[char]))
            return encoded_text

        def EC_Key_1():
            s = randprime(1, p)
            while s == n:
                s = randprime(1, p)
            public_key = multiply_ell(G[0],G[1],s)
            private_key = s
            return public_key, private_key

        def crypt(ell_points_result,EC_a_private_key):
            result = []
            s = EC_a_private_key
            while s == n:
                s = randprime(1, p)
            R = multiply_ell(EC_public_key[0],EC_public_key[1],s)
            extracted_points = [[point[0], point[1], point[2]] for point in ell_points_result]
            for i in extracted_points:
                k = i[0]
                x = i[1]
                y = i[2]
                crypt_result = summa_ell(R[0], R[1], x, y)
                result.append([k,crypt_result])
            return result

        def decrypt(encrypt_result,EC_private_key,EC_a_public_key):
            list = []
            new_list = []
            decrypt_result = []
            s = EC_private_key
           #EC_a_public_key, EC_a_private_key = EC_Key_1()
            R = multiply_ell(EC_a_public_key[0], EC_a_public_key[1], s)
            for item in encrypt_result:
                k = item[0]
                x = item[1][0]
                y = item[1][1]
                result = summa_ell(x,y,R[0],-R[1])
                list.append([k,result])
            #print(f"A_0 = Q - R: {list}")
            for i in list:
                x = i[1][0] - i[0]
                new_list.append(x)
            #print(f"x = x - k: {new_list}")
            for x in new_list:
                M = pow(x,RSA_private_key[1],RSA_private_key[0])
                decrypt_result.append(M)
            return decrypt_result

        decoding_dict = {value: key for key, value in encoding_dict.items()}
        def deencode_text(decoding_dict,deencrypt_result):
            decoded_text = ''
            for code in deencrypt_result:
                if int(code) in decoding_dict:
                    decoded_text += decoding_dict[int(code)]
            return decoded_text


        RSA_public_key, RSA_private_key = RSA_key()
        print(f"Открытый ключ RSA получателя: {RSA_public_key}")
        print(f"Секретный ключ RSA получателя: {RSA_private_key}")

        EC_public_key, EC_private_key = EC_Key()
        print(f"Открытый EC-ключ получателя: {EC_public_key}")
        print(f"Секретный EC-ключ получателя: {EC_private_key}")

        EC_a_public_key, EC_a_private_key = EC_Key_1()
        print(f"Открытый EC-ключ отправителя: {EC_a_public_key}")
        print(f"Секретный EC-ключ отправителя: {EC_a_private_key}")

        text = encode_text(encoding_dict)
        print(f"Закодированный текст: {text}")

        ell_points_result = points(text, RSA_public_key, ell_points)
        print(f"Преобразованный текст на точки эллиптической кривой: {ell_points_result}")

        encrypt_result = crypt(ell_points_result,EC_a_private_key)
        print(f"Зашифрованное сообщение: {encrypt_result}")

        deencrypt_result = decrypt(encrypt_result,EC_private_key,EC_a_public_key)
        print(f"Дешифрованное сообщение в виде кодированных чисел: {deencrypt_result}")

        deencode_result = deencode_text(decoding_dict,deencrypt_result)
        print(f"Дешифрованное сообщение в виде открытого текста: {deencode_result}")

ell_main()



