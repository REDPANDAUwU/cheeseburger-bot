import random


def generate_sentence():
    text = open('./input.txt').read()

    text_list = text.split('\n')

    # rebuild text_list
    new_text_list = []
    for i in text_list:
        if i.strip() != '' and i.strip('\n') != '':
            new_text_list.append(i.strip())
    text_list = new_text_list
    # print(text_list)

    # figure out max length of a message
    the_max = 0
    for i in text_list:
        if len(i) > the_max:
            the_max = len(i)

    comp_sentence = ''
    sentence_length = random.randint(3, the_max)

    iterations = 0
    meowing = True
    while meowing:
        iterations += 1
        try:
            # goes through sentences lookign for stuffs
            sentence = text_list[random.randint(0, len(text_list))]
            word = sentence.split()
            comp_sentence += str(word[0]) + ' '

            # rebuild the text_list
            new_text_list = []
            for i in text_list:
                # input(text_list)
                # print(1)
                # print(i)
                s = i.split()
                del s[0]
                # print(s)
                # print(s)
                meowe = ''
                for m in s:
                    meowe += f"{m} "
                # print(meowe)
                # input()
                # print(meowe)
                if meowe.strip() == '' or meowe == ' ':
                    pass
                else:
                    new_text_list.append(meowe)
            # print(2)
            # print(new_text_list)
            text_list = new_text_list
            # print(text_list)
        except IndexError:
            pass

        # check to end loop
        if len(text_list) == 0 or iterations > sentence_length:
            meowing = False

    return comp_sentence
