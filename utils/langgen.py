import random
import collections


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
        choices = {}
        # new_word = random.choice(datatable[picking_word.lower()])
        for i in datatable[picking_word.lower()]:
            if i in choices.keys():
                choices[i] += 1
            else:
                choices[i] = 1
        # print(choices)
        m = collections.Counter(choices)
        new_words = m.most_common(3)
        # input(new_words)
        new_word = random.choice(new_words)[0]

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


def generate_sentence(datatable):
    sentence_length = random.randint(10, 20)

    # datatable = generate_datatable(text_list)

    comp_sentence = ''

    meowing = True
    while meowing:
        comp_sentence = pick_words(datatable, sentence_length)
        if comp_sentence.strip() == '':
            pass
        else:
            meowing = False

    return comp_sentence


if __name__ == "__main__":
    text = open('./input.txt').read()

    text_list = text.split('\n')

    # rebuild text_list
    new_text_list = []
    for i in text_list:
        if i.strip() != '' and i.strip('\n') != '':
            new_text_list.append(i.strip())
    text_list = new_text_list

    datatable = generate_datatable(text_list)
    print(generate_sentence(datatable))
