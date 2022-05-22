import random


def generate_datatable(text):
    dictionary = {}
    for message in text:
        for i, word in enumerate(message.split()):
            # print(message.split())
            if word in dictionary.keys():
                # print(dictionary)
                # print(word)
                if len(message.split()) == i + 1:
                    # dictionary[word] = dictionary[word].append("TG_ENDING")
                    dictionary[word.lower()].append("TG_ENDING")
                else:
                    # dictionary[word] = dictionary[word].append(message.split()[i + 1])
                    dictionary[word.lower()].append(message.split()[i + 1])
            else:
                if len(message.split()) == i + 1:
                    dictionary[word.lower()] = ["TG_ENDING"]
                else:
                    dictionary[word.lower()] = [message.split()[i + 1]]

    return dictionary


def pick_words(datatable, sentence_length):
    comp_sentence = ''

    picking_word = random.choice(list(datatable.keys()))
    iterations = 0
    meowing = True
    while meowing:
        iterations += 1
        new_word = random.choice(datatable[picking_word.lower()])
        # print(starting_word)
        if new_word == "TG_ENDING":
            if random.randint(1, 7) == 2:
                meowing = False
            else:
                picking_word = random.choice(list(datatable.keys()))
        else:
            comp_sentence += new_word + ' '
            picking_word = new_word
        if iterations > sentence_length:
            meowing = False


    return comp_sentence


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

    sentence_length = random.randint(3, the_max)

    datatable = generate_datatable(text_list)

    comp_sentence = ''

    meowing = True
    while meowing:
        comp_sentence = pick_words(datatable, sentence_length)
        if comp_sentence.strip() == '':
            pass
        else:
            meowing = False

    return comp_sentence


def generate_sentence_old():
    text = open('./input.txt').read()

    text_list = text.split('\n')

    # rebuild text_list
    new_text_list = []
    for i in text_list:
        if i.strip() != '' and i.strip('\n') != '':
            new_text_list.append(i.strip())
    text_list = new_text_list
    # print(text_list)

    input(generate_datatable(text_list))

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


if __name__ == "__main__":
    print(generate_sentence())
